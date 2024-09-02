import asyncio

import edge_tts

TEXT = "她看了看表，距离这一次排练结束还有一个小时的时间。丰川祥子皱起眉头，举起手：“各位辛苦了，我们先休息五分钟。过一会儿再来。睦，干得很好。若麦，海玲，你们的表现实在是令我惊喜。初华你今天状态不太对，别着急，慢慢来。今天失误主要是我的问题，耽误了各位的时间十分抱歉。我会努力调整一下的。”说完话，她转过身，无视了睦关切的目光和初华探询的问候，一个人走向盥洗室。"
VOICE = "zh-CN-YunyangNeural"
OUTPUT_FILE = "test44.mp3"


async def amain() -> None:
    """Main function"""
    communicate = edge_tts.Communicate(TEXT, VOICE)
    with open(OUTPUT_FILE, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                print(f"WordBoundary: {chunk}")


if __name__ == "__main__":
    asyncio.run(amain())