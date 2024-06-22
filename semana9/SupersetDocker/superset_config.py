# Specify the App icon
APP_ICON = "/static/assets/images/edvai_logo.png"

DEFAULT_FEATURE_FLAGS: dict[str, bool] = {
    # When using a recent version of Druid that supports JOINs turn this on
    "DRUID_JOINS": False,
    "DYNAMIC_PLUGINS": False,
    # With Superset 2.0, we are updating the default so that the legacy datasource
    # editor no longer shows. Currently this is set to false so that the editor
    # option does show, but we will be depreciating it.
    "DISABLE_LEGACY_DATASOURCE_EDITOR": True,
    "ENABLE_TEMPLATE_PROCESSING": False,
    # Allow for javascript controls components
    # this enables programmers to customize certain charts (like the
    # geospatial ones) by inputting javascript in controls. This exposes
    # an XSS security vulnerability
    "ENABLE_JAVASCRIPT_CONTROLS": False,  # deprecated
    "KV_STORE": False,  # deprecated
    # When this feature is enabled, nested types in Presto will be
    # expanded into extra columns and/or arrays. This is experimental,
    # and doesn't work with all nested types.
    "PRESTO_EXPAND_DATA": False,
    # Exposes API endpoint to compute thumbnails
    "THUMBNAILS": False,
    "SHARE_QUERIES_VIA_KV_STORE": False,
    "TAGGING_SYSTEM": False,
    "SQLLAB_BACKEND_PERSISTENCE": True,
    "LISTVIEWS_DEFAULT_CARD_VIEW": False,
    # When True, this escapes HTML (rather than rendering it) in Markdown components
    "ESCAPE_MARKDOWN_HTML": False,
    "DASHBOARD_CROSS_FILTERS": True,  # deprecated
    "DASHBOARD_VIRTUALIZATION": True,
    "GLOBAL_ASYNC_QUERIES": False,
    "EMBEDDED_SUPERSET": True,
    # Enables Alerts and reports new implementation
    "ALERT_REPORTS": False,
    "ALERT_REPORT_TABS": False,
    "DASHBOARD_RBAC": False,
    "ENABLE_ADVANCED_DATA_TYPES": False,
    # Enabling ALERTS_ATTACH_REPORTS, the system sends email and slack message
    # with screenshot and link
    # Disables ALERTS_ATTACH_REPORTS, the system DOES NOT generate screenshot
    # for report with type 'alert' and sends email and slack message with only link;
    # for report with type 'report' still send with email and slack message with
    # screenshot and link
    "ALERTS_ATTACH_REPORTS": True,
    # Allow users to export full CSV of table viz type.
    # This could cause the server to run out of memory or compute.
    "ALLOW_FULL_CSV_EXPORT": False,
    "ALLOW_ADHOC_SUBQUERY": True,
    "USE_ANALAGOUS_COLORS": True,
    # Apply RLS rules to SQL Lab queries. This requires parsing and manipulating the
    # query, and might break queries and/or allow users to bypass RLS. Use with care!
    "RLS_IN_SQLLAB": False,
    # Enable caching per impersonation key (e.g username) in a datasource where user
    # impersonation is enabled
    "CACHE_IMPERSONATION": False,
    # Enable caching per user key for Superset cache (not database cache impersonation)
    "CACHE_QUERY_BY_USER": False,
    # Enable sharing charts with embedding
    "EMBEDDABLE_CHARTS": True,
    "DRILL_TO_DETAIL": True,
    "DRILL_BY": True,
    "DATAPANEL_CLOSED_BY_DEFAULT": False,
    "HORIZONTAL_FILTER_BAR": False,
    # The feature is off by default, and currently only supported in Presto and Postgres,
    # and Bigquery.
    # It also needs to be enabled on a per-database basis, by adding the key/value pair
    # `cost_estimate_enabled: true` to the database `extra` attribute.
    "ESTIMATE_QUERY_COST": False,
    # Allow users to enable ssh tunneling when creating a DB.
    # Users must check whether the DB engine supports SSH Tunnels
    # otherwise enabling this flag won't have any effect on the DB.
    "SSH_TUNNELING": True,
    "AVOID_COLORS_COLLISION": True,
    # Do not show user info in the menu
    "MENU_HIDE_USER_INFO": False,
    # Allows users to add a ``superset://`` DB that can query across databases. This is
    # an experimental feature with potential security and performance risks, so use with
    # caution. If the feature is enabled you can also set a limit for how much data is
    # returned from each database in the ``SUPERSET_META_DB_LIMIT`` configuration value
    # in this file.
    "ENABLE_SUPERSET_META_DB": False,
    # Set to True to replace Selenium with Playwright to execute reports and thumbnails.
    # Unlike Selenium, Playwright reports support deck.gl visualizations
    # Enabling this feature flag requires installing "playwright" pip package
    "PLAYWRIGHT_REPORTS_AND_THUMBNAILS": False,
    # Set to True to enable experimental chart plugins
    "CHART_PLUGINS_EXPERIMENTAL": False,
}


THEME_OVERRIDES = {
    
    "colors": {

        "text": {
            "label": '#879399',
            "help": '#737373'
        },

        "primary": {
            "base": 'red',
        },
        "secondary": {
            "base": 'green',
        },
        "grayscale": {
            "base": 'orange',
        },
        "error":{
            "base": 'Pink'
        }
    },


    "typography": {
        "families": {
            "monospace": "Courier New, Courier, monospace"
        },
        "weights": {
            "normal": 400
        },
        "colors": {
            "text": "#00FF00"
            "background": "#000000"
        }
    }
}