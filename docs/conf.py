project = "RoSHI"
copyright = "2026, JIRL Lab, University of Pennsylvania"
author = "Wenjing Mao, Jefferson Ng, Luyang Hu, Daniel Gehrig, Antonio Loquercio"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]

html_theme_options = {
    "logo": {
        "text": "RoSHI",
    },
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/Jirl-upenn/RoSHI-App",
            "icon": "fa-brands fa-github",
        },
    ],
    "navbar_align": "left",
    "show_prev_next": True,
    "navigation_with_keys": True,
}

html_context = {
    "default_mode": "light",
}
