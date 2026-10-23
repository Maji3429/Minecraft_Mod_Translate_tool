"""Regression tests for Flet 1.0 UI component builders."""

import unittest
from unittest.mock import MagicMock

import flet as ft

from src.ui import app, components, styles


class UiComponentBuilderTests(unittest.TestCase):
    """Verify UI controls construct cleanly with Flet 1.0 APIs."""

    def test_styles_builders(self):
        theme = styles.create_theme()
        self.assertIsInstance(theme, ft.Theme)

        page = MagicMock(spec=ft.Page)
        status_container, dot, status_text = components.create_ollama_status_indicator()
        self.assertIsInstance(status_container, ft.Container)
        self.assertIsInstance(dot, ft.Container)
        self.assertIsInstance(status_text, ft.Text)

        app_bar = styles.create_app_bar(page, status_widget=status_container)
        self.assertIsInstance(app_bar, ft.AppBar)

        btn = styles.create_button("Test", ft.Icons.ATTACH_FILE)
        self.assertIsInstance(btn, ft.TextButton)

        dropdown = styles.create_dropdown("Version", ["1.20.1", "1.21.1"])
        self.assertIsInstance(dropdown, ft.Dropdown)
        self.assertEqual(len(dropdown.options), 2)

        card = styles.create_card(ft.Text("Body"))
        self.assertIsInstance(card, ft.Card)

    def test_dialogs_and_progress_controls(self):
        page = MagicMock()
        page.data = {}
        page.window = MagicMock()
        page.window.height = 700
        page.controls = []

        loading = components.make_loading_indicator(page)
        self.assertIsInstance(loading, ft.Container)

        pb, info = components.make_extract_progress(page)
        self.assertIsInstance(pb, ft.ProgressBar)
        self.assertIsInstance(info, ft.Text)

        pb2, info2 = components.make_progress_bar(page, "/tmp/mod/assets/modid/lang/en_us.json")
        self.assertIsInstance(pb2, ft.ProgressBar)
        self.assertIsInstance(info2, ft.Text)

        components.show_ollama_settings_dialog(page, lambda: None)
        components.show_ollama_not_found_dialog(page)
        components.show_model_not_found_dialog(page, "mitmul/plamo-2-translate")
        self.assertEqual(page.show_dialog.call_count, 3)

        translator_app = app.MinecraftModTranslatorApp()
        translator_app._show_corrupted_config_dialog(page)
        self.assertEqual(page.show_dialog.call_count, 4)
