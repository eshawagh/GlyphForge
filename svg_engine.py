def generate_svg(text):

    svg = f"""
    <svg width="800" height="200"
         xmlns="http://www.w3.org/2000/svg">

        <defs>
            <filter id="glow">
                <feGaussianBlur stdDeviation="4"
                                result="coloredBlur"/>

                <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
        </defs>

        <rect width="100%" height="100%" fill="black"/>

        <text
            x="50%"
            y="50%"
            fill="lime"
            font-size="40"
            text-anchor="middle"
            dominant-baseline="middle"
            font-family="monospace"
            filter="url(#glow)">

            {text}

        </text>

    </svg>
    """

    return svg