import streamlit as st

# Extended ghost character code points
GHOST_CHAR_CODES = {
    160: 'NO-BREAK SPACE (U+00A0)',
    8203: 'ZERO WIDTH SPACE (U+200B)',
    8239: 'NARROW NO-BREAK SPACE (U+202F)',
    8288: 'WORD JOINER (U+2060)',
    65279: 'ZERO WIDTH NO-BREAK SPACE / BOM (U+FEFF)',
    8204: 'ZERO WIDTH NON-JOINER (U+200C)',
    8205: 'ZERO WIDTH JOINER (U+200D)',
    6158: 'MONGOLIAN VOWEL SEPARATOR (U+180E)',
    1351: 'COMBINING GRAPHEME JOINER (U+034F)',
    8289: 'INVISIBLE PLUS (U+2061)',
    8290: 'INVISIBLE COMMA (U+2062)',
    8291: 'INVISIBLE TIMES (U+2063)',
    8292: 'INVISIBLE SEPARATOR (U+2064)',
    13: 'CARRIAGE RETURN (U+000D)',
    10: 'LINE FEED (U+000A)',
    8232: 'LINE SEPARATOR (U+2028)',
    8233: 'PARAGRAPH SEPARATOR (U+2029)',
    8192: 'EN QUAD (U+2000)',
    8193: 'EM QUAD (U+2001)',
    8194: 'EN SPACE (U+2002)',
    8195: 'EM SPACE (U+2003)',
    8196: 'THREE-PER-EM SPACE (U+2004)',
    8197: 'FOUR-PER-EM SPACE (U+2005)',
    8198: 'SIX-PER-EM SPACE (U+2006)',
    8199: 'FIGURE SPACE (U+2007)',
    8200: 'PUNCTUATION SPACE (U+2008)',
    8201: 'THIN SPACE (U+2009)',
    8202: 'HAIR SPACE (U+200A)',
    8234: 'LEFT-TO-RIGHT EMBEDDING (U+202A)',
    8235: 'RIGHT-TO-LEFT EMBEDDING (U+202B)',
    8236: 'LEFT-TO-RIGHT OVERRIDE (U+202D)',
    8237: 'RIGHT-TO-LEFT OVERRIDE (U+202E)',
    8238: 'POP DIRECTIONAL FORMATTING (U+202C)',
    8298: 'LEFT-TO-RIGHT ISOLATE (U+2066)',
    8299: 'RIGHT-TO-LEFT ISOLATE (U+2067)',
    8300: 'FIRST STRONG ISOLATE (U+2068)',
    8301: 'POP DIRECTIONAL ISOLATE (U+2069)',
    12288: 'IDEOGRAPHIC SPACE (U+3000)'
}

def get_codepoints(text):
    codepoints = []
    utf32 = text.encode('utf-32-be')
    for i in range(0, len(utf32), 4):
        chunk = utf32[i:i+4]
        code = int.from_bytes(chunk, byteorder='big')
        char = chunk.decode('utf-32-be')
        codepoints.append((i // 4, char, code))
    return codepoints

def detect_ghost_chars(text):
    found = []
    highlighted = ''
    for i, char, code in get_codepoints(text):
        if code in GHOST_CHAR_CODES:
            found.append(f"Position {i}: U+{code:04X} – {GHOST_CHAR_CODES[code]}")
            highlighted += f'<mark title="{GHOST_CHAR_CODES[code]}">{char}</mark>'
        else:
            highlighted += char
    return found, highlighted

def clean_ghost_chars(text):
    cleaned = ''
    for _, char, code in get_codepoints(text):
        if code not in GHOST_CHAR_CODES:
            cleaned += char
    return cleaned

st.set_page_config(page_title="Ghost Character Cleaner")
st.title("👻 Ghost Character Detector & Cleaner")

text_input = st.text_area("Paste your text below:", height=200)
col1, col2, col3 = st.columns(3)
analyze_pressed = col1.button("🔍 Analyze")
clean_pressed = col2.button("🧹 Clean")
autoclean_pressed = col3.button("⚡ Auto-Clean & Replace")

if text_input:
    if analyze_pressed:
        found, highlighted = detect_ghost_chars(text_input)
        if found:
            st.warning(f"⚠️ Found {len(found)} ghost character(s):")
            for line in found:
                st.text(line)
            st.markdown("### 🔎 Highlighted Text:", unsafe_allow_html=True)
            st.markdown(f"<pre>{highlighted}</pre>", unsafe_allow_html=True)
        else:
            st.success("✅ No ghost characters found.")
            st.markdown(f"<pre>{text_input}</pre>", unsafe_allow_html=True)

    elif clean_pressed:
        cleaned = clean_ghost_chars(text_input)
        st.success("✅ Cleaned Text:")
        st.code(cleaned)

    elif autoclean_pressed:
        cleaned = clean_ghost_chars(text_input)
        st.text_area("Cleaned Text:", cleaned, height=200)
        st.success("⚡ Auto-clean complete. Text replaced in input field.")
