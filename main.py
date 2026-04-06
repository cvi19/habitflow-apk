"""
HabitFlow APK — main.py
========================
Kivy app that renders the full HabitFlow UI via Android's native WebView.
Built with Buildozer → produces a real .apk file.
"""

import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass, cast
    from android.runnable import run_on_ui_thread
    from android import activity

    # Android Java classes
    PythonActivity   = autoclass('org.kivy.android.PythonActivity')
    WebView          = autoclass('android.webkit.WebView')
    WebViewClient    = autoclass('android.webkit.WebViewClient')
    WebSettings      = autoclass('android.webkit.WebSettings')
    FrameLayout      = autoclass('android.widget.FrameLayout')
    LayoutParams     = autoclass('android.view.ViewGroup$LayoutParams')
    View             = autoclass('android.view.View')
    Color            = autoclass('android.graphics.Color')
    WindowManager    = autoclass('android.view.WindowManager$LayoutParams')


class HabitFlowWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if platform == 'android':
            Clock.schedule_once(self._create_webview, 0.1)

    @run_on_ui_thread
    def _create_webview(self, *args):
        # Get the current Android activity
        act = PythonActivity.mActivity

        # ── Create WebView ──────────────────────────────────────
        wv = WebView(act)
        settings = wv.getSettings()

        # Enable JavaScript
        settings.setJavaScriptEnabled(True)

        # Enable DOM storage (for localStorage — our data store)
        settings.setDomStorageEnabled(True)

        # Enable database storage
        settings.setDatabaseEnabled(True)

        # Enable app cache
        settings.setAppCacheEnabled(True)
        cache_dir = act.getCacheDir().getAbsolutePath()
        settings.setAppCachePath(cache_dir)

        # Allow file access (to load local HTML from assets)
        settings.setAllowFileAccess(True)
        settings.setAllowFileAccessFromFileURLs(True)
        settings.setAllowUniversalAccessFromFileURLs(True)

        # Responsive layout
        settings.setUseWideViewPort(True)
        settings.setLoadWithOverviewMode(True)
        settings.setBuiltInZoomControls(False)
        settings.setDisplayZoomControls(False)

        # Smooth scrolling / overscroll
        wv.setOverScrollMode(View.OVER_SCROLL_NEVER)
        wv.setScrollBarStyle(View.SCROLLBARS_INSIDE_OVERLAY)

        # Dark background to avoid white flash on load
        wv.setBackgroundColor(Color.parseColor("#060610"))

        # Set a basic WebViewClient (handles navigation within the app)
        wv.setWebViewClient(WebViewClient())

        # ── Load the HTML from assets ────────────────────────────
        # Kivy packages 'assets/' folder contents into the APK
        # and they're accessible at file:///android_asset/
        wv.loadUrl("file:///android_asset/index.html")

        # ── Attach to the activity layout ───────────────────────
        layout = act.getWindow().getDecorView()
        frame = FrameLayout(act)
        params = LayoutParams(
            LayoutParams.MATCH_PARENT,
            LayoutParams.MATCH_PARENT
        )
        frame.addView(wv, params)
        act.addContentView(frame, params)

        # Make status bar color match app theme
        try:
            window = act.getWindow()
            window.addFlags(WindowManager.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
            window.setStatusBarColor(Color.parseColor("#060610"))
            window.setNavigationBarColor(Color.parseColor("#060610"))
        except Exception:
            pass


class HabitFlowApp(App):
    def build(self):
        # Black background widget while WebView loads
        widget = HabitFlowWidget()
        self.title = "HabitFlow"
        return widget


if __name__ == "__main__":
    HabitFlowApp().run()
