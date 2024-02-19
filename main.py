from utility import text_diff

def main():
    text1 = """Hello World!
    
The morning sets the tone for the rest of our day. A calm and structured start, with a healthy breakfast and a moment of mindfulness, can significantly boost our productivity and mood. Many find that planning their day in the morning helps in staying focused and achieving their goals more efficiently."""

    text2 = """Hello World.

The morning sets the tone for our entire day. A calm and structured beginning, with a nutritious breakfast and a brief period of mindfulness, significantly boosts our productivity and mood. Adding exercise, such as a quick walk, amplifies this positive impact. Many find that planning their day in the morning helps in staying focused and achieving their goals more efficiently.

This is the third paragraph..."""
#     text1 = """Hello World. 
# This is the first text."""

#     text2 = """Hi World!
# This is the second text!"""

    text_diff(text2, text1)

if __name__ == "__main__":
    main()