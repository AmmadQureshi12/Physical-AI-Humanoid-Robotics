"""
Script to index book content into the Qdrant vector database.
"""
import asyncio
import argparse
import os
from pathlib import Path
import re
import time


async def index_book_content(book_path: str):
    """
    Index book content from the specified path into the vector database.

    Args:
        book_path: Path to the book content directory
    """
    # Import here to avoid circular dependencies
    from src.services.document_processor import document_processor

    print(f"Indexing book content from: {book_path}")

    book_content = []

    # Walk through the book directory to find all content files
    book_dir = Path(book_path)

    # Look for markdown files in the docs directory structure
    docs_dir = book_dir / "docs"

    if not docs_dir.exists():
        print(f"Warning: {docs_dir} does not exist. Looking for markdown files in {book_dir}")
        # If docs directory doesn't exist, look for markdown files in the root
        md_files = list(book_dir.rglob("*.md"))
    else:
        md_files = list(docs_dir.rglob("*.md"))

    print(f"Found {len(md_files)} markdown files to process")

    for file_path in md_files:
        print(f"Processing: {file_path}")

        # Extract chapter info from the path
        relative_path = file_path.relative_to(book_dir)
        path_parts = relative_path.parts

        # Determine chapter and section from the file path
        chapter_info = {
            "chapter_number": 0,
            "chapter_title": "Unknown",
            "section_number": "Unknown",
            "section_title": ""
        }

        # Parse the path to extract chapter information
        if len(path_parts) >= 2:
            # Path format: docs/chapter-XX-name/file.md
            chapter_part = path_parts[1] if path_parts[0] == "docs" else path_parts[0]

            # Extract chapter number and title from directory name
            chapter_match = re.match(r'chapter-(\d+)-(.+)', chapter_part)
            if chapter_match:
                chapter_info["chapter_number"] = int(chapter_match.group(1))
                chapter_info["chapter_title"] = chapter_match.group(2).replace('-', ' ').title()

        # Add specific section info based on filename
        filename = file_path.stem
        if filename == "index":
            chapter_info["section_number"] = f"{chapter_info['chapter_number']}.1"
            chapter_info["section_title"] = "Introduction"
        elif filename == "spec":
            chapter_info["section_number"] = f"{chapter_info['chapter_number']}.2"
            chapter_info["section_title"] = "Specification"
        elif filename == "exercises":
            chapter_info["section_number"] = f"{chapter_info['chapter_number']}.3"
            chapter_info["section_title"] = "Exercises"
        elif filename == "troubleshooting":
            chapter_info["section_number"] = f"{chapter_info['chapter_number']}.4"
            chapter_info["section_title"] = "Troubleshooting"
        else:
            chapter_info["section_number"] = f"{chapter_info['chapter_number']}.5"
            chapter_info["section_title"] = filename.replace('-', ' ').title()

        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove markdown headers and metadata if present
        # Look for YAML frontmatter and remove it
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

        # Split content into chunks based on headers
        # This regex splits on markdown headers but keeps them with the content
        header_split = re.split(r'(\n##\s+.*?\n|\n###\s+.*?\n)', content)

        current_header = ""
        for part in header_split:
            if part.strip() == "":
                continue

            # Check if this part is a header
            if re.match(r'\n##\s+.*?\n|\n###\s+.*?\n', part):
                current_header = part.strip()
            else:
                # This is content following a header
                full_content = current_header + "\n" + part if current_header else part

                # Only add content that has substantial text (more than just headers)
                text_only = re.sub(r'\n#+\s+', ' ', full_content).strip()
                if len(text_only) > 50:  # Only include chunks with substantial content
                    chunk = {
                        "content": full_content.strip(),
                        "chapter_number": chapter_info["chapter_number"],
                        "chapter_title": chapter_info["chapter_title"],
                        "section_number": chapter_info["section_number"],
                        "section_title": chapter_info["section_title"] + (" - " + current_header.strip() if current_header else ""),
                        "page_start": 1  # Markdown files don't have pages, using 1 as default
                    }
                    book_content.append(chunk)

    print(f"Processing {len(book_content)} content chunks for indexing...")

    # Process and index the content with rate limiting
    success = await process_and_index_with_rate_limiting(document_processor, book_content)

    if success:
        print(f"Successfully indexed {len(book_content)} content chunks into the vector database")
    else:
        print("Failed to index content into the vector database")

    return success


async def process_and_index_with_rate_limiting(document_processor, book_content):
    """
    Process and index content with rate limiting to avoid API limits.
    """
    import asyncio
    from src.core.exceptions import AppBaseException

    # Process content in batches to respect API rate limits
    batch_size = 10  # Conservative batch size to stay under rate limits
    total_chunks = len(book_content)

    for i in range(0, total_chunks, batch_size):
        batch = book_content[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1} of {(total_chunks + batch_size - 1)//batch_size}")

        try:
            # Process the batch
            success = await document_processor.process_and_index_book_content(batch)

            if not success:
                print(f"Failed to process batch {i//batch_size + 1}")
                return False

        except Exception as e:
            print(f"Error processing batch {i//batch_size + 1}: {str(e)}")
            # If it's a rate limit error, wait longer before continuing
            if "rate" in str(e).lower() or "429" in str(e):
                print("Rate limit hit, waiting 60 seconds before continuing...")
                await asyncio.sleep(60)
                # Try again with the same batch
                try:
                    success = await document_processor.process_and_index_book_content(batch)
                    if not success:
                        print(f"Failed to process batch {i//batch_size + 1} after rate limit delay")
                        return False
                except Exception as retry_error:
                    print(f"Retry failed for batch {i//batch_size + 1}: {str(retry_error)}")
                    return False
            else:
                return False

        # Add delay between batches to respect rate limits
        print("Waiting 10 seconds before processing next batch...")
        await asyncio.sleep(10)

    return True


def main():
    parser = argparse.ArgumentParser(description="Index book content into the vector database")
    parser.add_argument(
        "--book-path",
        type=str,
        required=True,
        help="Path to the book content directory"
    )
    
    args = parser.parse_args()
    
    # Run the async function
    result = asyncio.run(index_book_content(args.book_path))
    
    if result:
        print("Book content indexing completed successfully!")
        exit(0)
    else:
        print("Book content indexing failed!")
        exit(1)


if __name__ == "__main__":
    main()