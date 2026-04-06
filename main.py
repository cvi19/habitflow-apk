"""
HabitFlow - main.py (Fixed)
Simple, reliable WebView approach for Android.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.utils import platform


# ── Only import Android stuff when running on Android ────────
if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread

    # Java classes we need
    PythonActivity  = autoclass('org.kivy.android.PythonActivity')
    WebView         = autoclass('android.webkit.WebView')
    WebViewClient   = autoclass('android.webkit.WebViewClient')
    LinearLayout    = autoclass('android.widget.LinearLayout')
    LayoutParams    = autoclass('android.view.ViewGroup$LayoutParams')
    Color           = autoclass('android.graphics.Color')
    View            = autoclass('android.view.View')


# ── This MUST be a module-level function (not a method) ──────
# run_on_ui_thread only works reliably at module level
if platform == 'android':
    @run_on_ui_thread
    def _create_webview(*args):
        activity = PythonActivity.mActivity

        # Create WebView
        wv = WebView(activity)
        s  = wv.getSettings()

        # Core settings
        s.setJavaScriptEnabled(True)
        s.setDomStorageEnabled(True)          # localStorage support
        s.setDatabaseEnabled(True)

        # Allow loading local HTML file
        s.setAllowFileAccess(True)
        s.setAllowFileAccessFromFileURLs(True)
        s.setAllowUniversalAccessFromFileURLs(True)

        # Fit content to screen
        s.setUseWideViewPort(True)
        s.setLoadWithOverviewMode(True)

        # Disable zoom controls (app handles it)
        s.setBuiltInZoomControls(False)
        s.setDisplayZoomControls(False)

        # Prevent white flash on load
        wv.setBackgroundColor(Color.parseColor('#060610'))

        # Keep navigation inside the WebView
        wv.setWebViewClient(WebViewClient())

        # Disable overscroll glow effect
        wv.setOverScrollMode(View.OVER_SCROLL_NEVER)

        # Load the bundled HTML from assets
        wv.loadUrl('file:///android_asset/index.html')

        # Fill the entire screen
        params = LayoutParams(
            LayoutParams.MATCH_PARENT,
            LayoutParams.MATCH_PARENT
        )

        # Wrap in a LinearLayout and set as the main view
        layout = LinearLayout(activity)
        layout.addView(wv, params)
        activity.setContentView(layout)


class HabitFlowApp(App):
    def build(self):
        if platform == 'android':
            # Schedule WebView creation on next frame
            # (activity must be fully ready first)
            Clock.schedule_once(_create_webview, 0.2)
        return Widget()


if __name__ == '__main__':
    HabitFlowApp().run()
