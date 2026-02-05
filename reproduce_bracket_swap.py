# -*- coding: utf-8 -*-
import arabic_reshaper
from bidi.algorithm import get_display

def test_brackets():
    reshaper = arabic_reshaper.ArabicReshaper(configuration={
        'delete_harakat': False,
        'support_ligatures': True
    })

    # U+FD3F ﴿ ORNATE RIGHT PARENTHESIS
    # U+FD3E ﴾ ORNATE LEFT PARENTHESIS
    
    # Logical intent: Open (Start) with FD3F, Close (End) with FD3E
    # RTL Text: [Start] TEXT [End]
    text = "\uFD3F" + " الله " + "\uFD3E"
    
    print(f"Original: {text}")
    print(f"Hex Original: {[hex(ord(c)) for c in text]}")
    
    reshaped = reshaper.reshape(text)
    bidi_text = get_display(reshaped)
    
    print(f"Bidi Output: {bidi_text}")
    print(f"Hex Bidi: {[hex(ord(c)) for c in bidi_text]}")
    
    # Check what is at the end of the string (Visual Right)
    # The last character in Python string should be displayed on the Right if printed normally?
    # No, get_display returns Visual string (LTR storage).
    # So index 0 is Left. Index -1 is Right.
    left_char = bidi_text[0]
    right_char = bidi_text[-1]
    
    print(f"Visual Left (End): {hex(ord(left_char))} - Should be FD3E (Left Paryn)")
    print(f"Visual Right (Start): {hex(ord(right_char))} - Should be FD3F (Right Paryn)")
    
    if ord(right_char) == 0xFD3E:
        print("FAIL: The Start bracket (Right) became FD3E (Left) due to mirroring!")
    elif ord(right_char) == 0xFD3F:
        print("SUCCESS: The Start bracket remained FD3F.")
        
if __name__ == "__main__":
    test_brackets()
