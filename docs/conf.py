project = "RoSHI"
copyright = "2026, JIRL Lab, University of Pennsylvania"
author = "Wenjing Mao, Jefferson Ng, Luyang Hu, Daniel Gehrig, Antonio Loquercio"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", ".venv", "Thumbs.db", ".DS_Store"]

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_show_sourcelink = False
html_favicon = "_static/favicon.png"

html_sidebars = {
    "**": ["sidebar-nav-bs"],
    "index": [],
}

html_theme_options = {
    "logo": {
        "image_light": "_static/roshi.png",
        "image_dark": "_static/roshi.png",
        "text": "RoSHI",
    },
    "icon_links": [
        {
            "name": "Project Page",
            "url": "https://roshi-mocap.github.io/",
            "icon": "fa-solid fa-house",
        },
        {
            "name": "GitHub",
            "url": "https://github.com/Jirl-upenn/RoSHI-MoCap",
            "icon": "fa-brands fa-github",
        },
    ],
    "navbar_align": "left",
    "show_prev_next": True,
    "navigation_with_keys": True,
    "show_nav_level": 2,
    "navigation_depth": 2,
    "header_links_before_dropdown": 4,
    "secondary_sidebar_items": {
        "**": ["page-toc"],
        "index": [],
    },
}

html_context = {
    "default_mode": "dark",
}
