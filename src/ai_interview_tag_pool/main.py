"""
Main pipeline script for AI Interview Tag Pool
Orchestrates the flow from subtitle download to tagging to saving.
"""
from config import Config, get_config
from services import SubtitleService, TaggingService, StorageService


def main(video_url: str):
    config = get_config()
    subtitle_service = SubtitleService(config)
    tagging_service = TaggingService(config)
    storage_service = StorageService(config)

    # 1. Download subtitles
    subtitles_result = subtitle_service.execute(video_url)
    if not subtitles_result["success"]:
        print(f"[Error] Subtitle extraction failed: {subtitles_result['error']}")
        return
    
    subtitles = subtitles_result["data"]["subtitles"]

    # 2. Tag
    tag_result = tagging_service.execute(subtitles)
    if not tag_result["success"]:
        print(f"[Error] Tagging failed: {tag_result['error']}")
        return
    
    # 3. Save
    save_result = storage_service.execute(tag_result["data"], prefix="tagged_segments")
    if save_result["success"]:
        print(f"[Success] Results saved: {save_result['data']}")
    else:
        print(f"[Error] Saving failed: {save_result['error']}")

if __name__ == "__main__":
    # Example usage
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py <youtube_video_url>")
    else:
        main(sys.argv[1])
