def generate_svg(text, font="georgia"):

    font_map = {
        "georgia": "Georgia",
        "garamond": "Garamond",
        "cursive": "cursive",
        "mono": "monospace"
    }

    selected_font = font_map.get(font, "Georgia")

    svg = f"""
    <svg width="900" height="260" xmlns="http://www.w3.org/2000/svg">

        <defs>

            <filter id="glow">
                <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>

        </defs>

        <rect width="100%" height="100%" fill="#4A0404"/>

        <text
            x="50%"
            y="50%"
            fill="#FFE9E3"
            font-size="54"
            text-anchor="middle"
            dominant-baseline="middle"
            font-family="{selected_font}"
            filter="url(#glow)">

            {text}

        </text>

    </svg>
    """

    return svg