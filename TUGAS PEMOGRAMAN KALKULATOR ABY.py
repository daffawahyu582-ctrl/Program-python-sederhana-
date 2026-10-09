import math
import re

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Line, Ellipse
from kivy.core.window import Window
from kivy.utils import get_color_from_hex


Window.size = (380, 580)


# =========================================================
# ICON HISTORY
# =========================================================

class HistoryIcon(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)

        self.bind(
            pos=self.update_canvas,
            size=self.update_canvas
        )

    def update_canvas(self, *args):

        self.canvas.before.clear()

        with self.canvas.before:

            Color(1, 1, 1, 0.7)

            cx, cy = self.center_x, self.center_y

            r = min(self.width, self.height) * 0.28

            # Lingkaran
            Line(
                circle=(cx, cy, r),
                width=1.5
            )

            # Jarum menit
            Line(
                points=[
                    cx,
                    cy,
                    cx,
                    cy + r * 0.5
                ],
                width=1.5
            )

            # Jarum jam
            Line(
                points=[
                    cx,
                    cy,
                    cx - r * 0.4,
                    cy
                ],
                width=1.5
            )


# =========================================================
# ICON MENU
# =========================================================

class MenuIcon(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)

        self.bind(
            pos=self.update_canvas,
            size=self.update_canvas
        )

    def update_canvas(self, *args):

        self.canvas.before.clear()

        with self.canvas.before:

            Color(1, 1, 1, 0.7)

            cx, cy = self.center_x, self.center_y

            r = 2.5
            offset = 10

            Ellipse(
                pos=(cx - r, cy + offset - r),
                size=(r * 2, r * 2)
            )

            Ellipse(
                pos=(cx - r, cy - r),
                size=(r * 2, r * 2)
            )

            Ellipse(
                pos=(cx - r, cy - offset - r),
                size=(r * 2, r * 2)
            )


# =========================================================
# CUSTOM BUTTON
# =========================================================

class CustomButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ''
        self.background_down = ''

        self.font_size = '18sp'

        self.background_color = get_color_from_hex(
            '#252529'
        )

        self.color = get_color_from_hex(
            '#FFFFFF'
        )


# =========================================================
# KALKULATOR
# =========================================================

class FixedCalculator(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.orientation = 'vertical'

        self.padding = 15
        self.spacing = 10

        # Data kalkulator
        self.formula = ''
        self.history_list = []

        self.is_deg = True
        self.is_inv = False
        self.is_sci_open = False


        # =================================================
        # MENU ATAS
        # =================================================

        self.top_menu = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.08
        )


        # HISTORY
        self.btn_history = HistoryIcon(
            size_hint_x=0.15
        )

        self.btn_history.bind(
            on_press=self.show_history_popup
        )


        # SPACER
        self.menu_spacer = Label(
            size_hint_x=0.50
        )


        # TOMBOL KONVERSI
        self.btn_convert = CustomButton(
            text='Konversi',
            size_hint_x=0.25,
            font_size='13sp'
        )

        self.btn_convert.background_color = (
            get_color_from_hex('#3A3A5E')
        )

        self.btn_convert.color = (
            get_color_from_hex('#6FDFDF')
        )

        self.btn_convert.bind(
            on_press=self.show_conversion_popup
        )


        # MENU SCIENTIFIC
        self.btn_more = MenuIcon(
            size_hint_x=0.15
        )

        self.btn_more.bind(
            on_press=self.toggle_scientific_panel
        )


        # Masukkan ke menu
        self.top_menu.add_widget(
            self.btn_history
        )

        self.top_menu.add_widget(
            self.menu_spacer
        )

        self.top_menu.add_widget(
            self.btn_convert
        )

        self.top_menu.add_widget(
            self.btn_more
        )


        self.add_widget(
            self.top_menu
        )


        # =================================================
        # DISPLAY
        # =================================================

        self.display = Label(
            text='0',
            font_size='38sp',
            halign='right',
            valign='middle',
            size_hint_y=0.20,
            color=get_color_from_hex('#6FDFDF'),
            bold=True
        )

        self.display.bind(
            size=self._update_text_size
        )

        self.add_widget(
            self.display
        )


        # =================================================
        # SCIENTIFIC PANEL
        # =================================================

        self.scientific_grid = GridLayout(
            cols=4,
            spacing=8,
            size_hint_y=0.35
        )


        self.sci_buttons_data = [

            ('√', '√('),
            ('π', 'π'),
            ('^', '^'),
            ('!', '!'),

            ('Deg', 'Deg'),
            ('sin', 'sin('),
            ('cos', 'cos('),
            ('tan', 'tan('),

            ('Inv', 'Inv'),
            ('e', 'e'),
            ('ln', 'ln('),
            ('log', 'log(')

        ]


        self.sci_button_widgets = {}


        for text, val in self.sci_buttons_data:

            btn = CustomButton(
                text=text
            )

            btn.background_color = (
                get_color_from_hex('#3A3A5E')
            )

            btn.color = (
                get_color_from_hex('#6FDFDF')
            )

            btn.bind(
                on_press=lambda instance, t=text:
                self.on_sci_click(t)
            )

            self.sci_button_widgets[text] = btn

            self.scientific_grid.add_widget(
                btn
            )


        # =================================================
        # TOMBOL KALKULATOR UTAMA
        # =================================================

        self.buttons_grid = GridLayout(
            cols=4,
            spacing=10,
            size_hint_y=0.72
        )


        button_layout = [

            ('C', '#950740'),
            ('AC', '#950740'),
            ('%', '#4E4E50'),
            (':', '#4E4E50'),

            ('7', '#252529'),
            ('8', '#252529'),
            ('9', '#252529'),
            ('x', '#4E4E50'),

            ('4', '#252529'),
            ('5', '#252529'),
            ('6', '#252529'),
            ('-', '#4E4E50'),

            ('1', '#252529'),
            ('2', '#252529'),
            ('3', '#252529'),
            ('+', '#4E4E50'),

            (',', '#252529'),
            ('0', '#252529'),
            ('.', '#252529'),
            ('=', '#6FDFDF')

        ]


        for text, bg_color in button_layout:

            btn = CustomButton(
                text=text
            )

            btn.background_color = (
                get_color_from_hex(bg_color)
            )

            if text == '=':

                btn.color = (
                    get_color_from_hex('#000000')
                )

            btn.bind(
                on_press=self.on_button_click
            )

            self.buttons_grid.add_widget(
                btn
            )


        self.add_widget(
            self.buttons_grid
        )


    # =========================================================
    # UPDATE DISPLAY
    # =========================================================

    def _update_text_size(self, instance, value):

        self.display.text_size = (
            self.display.width - 20,
            None
        )


    # =========================================================
    # SCIENTIFIC PANEL
    # =========================================================

    def toggle_scientific_panel(self, instance):

        if not self.is_sci_open:

            self.remove_widget(
                self.buttons_grid
            )

            self.add_widget(
                self.scientific_grid
            )

            self.add_widget(
                self.buttons_grid
            )

            self.buttons_grid.size_hint_y = 0.55

            self.is_sci_open = True

        else:

            self.remove_widget(
                self.scientific_grid
            )

            self.buttons_grid.size_hint_y = 0.72

            self.is_sci_open = False


    # =========================================================
    # TOMBOL SCIENTIFIC
    # =========================================================

    def on_sci_click(self, text):

        # DEG / RAD
        if text in ['Deg', 'Rad']:

            self.is_deg = not self.is_deg

            new_mode = (
                'Deg'
                if self.is_deg
                else 'Rad'
            )

            self.sci_button_widgets[
                'Deg'
            ].text = new_mode

            return


        # INV
        if text == 'Inv':

            self.is_inv = not self.is_inv

            self.sci_button_widgets[
                'Inv'
            ].background_color = (

                get_color_from_hex('#6FDFDF')
                if self.is_inv
                else get_color_from_hex('#3A3A5E')
            )

            self.sci_button_widgets[
                'Inv'
            ].color = (

                get_color_from_hex('#000000')
                if self.is_inv
                else get_color_from_hex('#6FDFDF')
            )


            self.sci_button_widgets[
                'sin'
            ].text = (
                'asin'
                if self.is_inv
                else 'sin'
            )

            self.sci_button_widgets[
                'cos'
            ].text = (
                'acos'
                if self.is_inv
                else 'cos'
            )

            self.sci_button_widgets[
                'tan'
            ].text = (
                'atan'
                if self.is_inv
                else 'tan'
            )

            return


        input_text = text


        if self.is_inv and text in [
            'sin',
            'cos',
            'tan'
        ]:

            input_text = 'a' + text


        if input_text in [
            'sin',
            'cos',
            'tan',
            'asin',
            'acos',
            'atan',
            'ln',
            'log',
            '√'
        ]:

            append_val = input_text + '('

        else:

            append_val = input_text


        if self.display.text in [
            '0',
            'Error'
        ]:

            self.formula = append_val

        else:

            self.formula += append_val


        self.display.text = self.formula


    # =========================================================
    # KONVERSI BILANGAN
    # =========================================================

    def show_conversion_popup(self, instance):

        popup = ModalView(
            size_hint=(0.92, 0.82)
        )


        content = BoxLayout(
            orientation='vertical',
            padding=12,
            spacing=8
        )


        # -----------------------------------------------------
        # JUDUL
        # -----------------------------------------------------

        title = Label(
            text='Konversi Bilangan',
            font_size='22sp',
            bold=True,
            color=get_color_from_hex('#6FDFDF'),
            size_hint_y=0.12
        )

        content.add_widget(
            title
        )


        # -----------------------------------------------------
        # INPUT ANGKA
        # -----------------------------------------------------

        input_number = TextInput(
            text='190',
            multiline=False,
            font_size='22sp',
            halign='center',
            size_hint_y=0.11
        )

        content.add_widget(
            input_number
        )


        selected_base = {
            'value': 10
        }


        # =====================================================
        # HASIL KONVERSI
        # =====================================================

        result_grid = GridLayout(
            cols=2,
            spacing=7,
            size_hint_y=0.40
        )


        # DEC
        dec_label = Label(
            text='DEC',
            font_size='16sp',
            color=get_color_from_hex('#6FDFDF')
        )

        dec_result = TextInput(
            text='-',
            readonly=True,
            multiline=False,
            font_size='17sp'
        )


        # BIN
        bin_label = Label(
            text='BIN',
            font_size='16sp',
            color=get_color_from_hex('#6FDFDF')
        )

        bin_result = TextInput(
            text='-',
            readonly=True,
            multiline=False,
            font_size='17sp'
        )


        # OCT
        oct_label = Label(
            text='OCT',
            font_size='16sp',
            color=get_color_from_hex('#6FDFDF')
        )

        oct_result = TextInput(
            text='-',
            readonly=True,
            multiline=False,
            font_size='17sp'
        )


        # HEX
        hex_label = Label(
            text='HEX',
            font_size='16sp',
            color=get_color_from_hex('#6FDFDF')
        )

        hex_result = TextInput(
            text='-',
            readonly=True,
            multiline=False,
            font_size='17sp'
        )


        # Masukkan ke grid
        result_grid.add_widget(
            dec_label
        )

        result_grid.add_widget(
            dec_result
        )


        result_grid.add_widget(
            bin_label
        )

        result_grid.add_widget(
            bin_result
        )


        result_grid.add_widget(
            oct_label
        )

        result_grid.add_widget(
            oct_result
        )


        result_grid.add_widget(
            hex_label
        )

        result_grid.add_widget(
            hex_result
        )


        content.add_widget(
            result_grid
        )


        # =====================================================
        # TOMBOL
        # =====================================================

        button_grid = BoxLayout(
            orientation='horizontal',
            spacing=8,
            size_hint_y=0.10
        )


        btn_convert = Button(
            text='Konversi',
            font_size='17sp',
            background_normal='',
            background_color=
            get_color_from_hex('#6FDFDF'),

            color=
            get_color_from_hex('#000000')
        )


        btn_close = Button(
            text='Tutup',
            font_size='17sp',
            background_normal='',
            background_color=
            get_color_from_hex('#950740')
        )


        button_grid.add_widget(
            btn_convert
        )

        button_grid.add_widget(
            btn_close
        )


        content.add_widget(
            button_grid
        )


        # =====================================================
        # PROSES KONVERSI
        # =====================================================

        def convert_number(instance):

            try:

                text = input_number.text.strip()


                if not text:

                    raise ValueError


                # Baca input sesuai basis
                value = int(
                    text,
                    selected_base['value']
                )


                # ---------------------------------------------
                # HASIL DEC
                # ---------------------------------------------

                dec_result.text = str(
                    value
                )


                # ---------------------------------------------
                # HASIL BIN
                # ---------------------------------------------

                bin_result.text = bin(
                    value
                )[2:]


                # ---------------------------------------------
                # HASIL OCT
                # ---------------------------------------------

                oct_result.text = oct(
                    value
                )[2:]


                # ---------------------------------------------
                # HASIL HEX
                # ---------------------------------------------

                hex_result.text = hex(
                    value
                )[2:].upper()


            except ValueError:

                dec_result.text = '-'
                bin_result.text = '-'
                oct_result.text = '-'
                hex_result.text = '-'


        btn_convert.bind(
            on_press=convert_number
        )


        btn_close.bind(
            on_press=popup.dismiss
        )


        popup.add_widget(
            content
        )

        popup.open()


    # =========================================================
    # HISTORY
    # =========================================================

    def show_history_popup(self, instance):

        popup = ModalView(
            size_hint=(0.85, 0.6)
        )


        content = BoxLayout(
            orientation='vertical',
            padding=15,
            spacing=10
        )


        title = Label(
            text='Riwayat Perhitungan',
            font_size='18sp',
            bold=True,
            size_hint_y=0.2,
            color=get_color_from_hex('#6FDFDF')
        )


        content.add_widget(
            title
        )


        history_text = (

            "\n".join(
                self.history_list[-5:]
            )

            if self.history_list

            else
            "Belum ada riwayat."
        )


        history_label = Label(
            text=history_text,
            halign='center',
            valign='middle',
            size_hint_y=0.6,
            font_size='16sp'
        )


        content.add_widget(
            history_label
        )


        btn_close = Button(
            text='Tutup',
            size_hint_y=0.2,
            background_normal='',
            background_color=
            get_color_from_hex('#950740')
        )


        btn_close.bind(
            on_press=popup.dismiss
        )


        content.add_widget(
            btn_close
        )


        popup.add_widget(
            content
        )

        popup.open()


    # =========================================================
    # MESIN PERHITUNGAN
    # =========================================================

    def evaluate_formula(self, expr):

        # Simbol dasar
        expr = expr.replace(
            '%',
            '/100'
        )

        expr = expr.replace(
            ':',
            '/'
        )

        expr = expr.replace(
            'x',
            '*'
        )

        expr = expr.replace(
            ',',
            '.'
        )

        expr = expr.replace(
            'π',
            'math.pi'
        )

        expr = expr.replace(
            'e',
            'math.e'
        )

        expr = expr.replace(
            '^',
            '**'
        )

        expr = expr.replace(
            '√(',
            'math.sqrt('
        )

        expr = expr.replace(
            'ln(',
            'math.log('
        )

        expr = expr.replace(
            'log(',
            'math.log10('
        )


        # Faktorial
        expr = re.sub(
            r'(\d+)!',
            r'math.factorial(\1)',
            expr
        )


        # =====================================================
        # TRIGONOMETRI
        # =====================================================

        def my_sin(x):

            val = (
                math.sin(math.radians(x))
                if self.is_deg
                else math.sin(x)
            )

            return round(
                val,
                12
            )


        def my_cos(x):

            val = (
                math.cos(math.radians(x))
                if self.is_deg
                else math.cos(x)
            )

            return round(
                val,
                12
            )


        def my_tan(x):

            if self.is_deg and (
                x % 180 == 90
            ):

                raise ValueError(
                    "Undefined"
                )


            val = (
                math.tan(math.radians(x))
                if self.is_deg
                else math.tan(x)
            )

            return round(
                val,
                12
            )


        def my_asin(x):

            val = math.asin(x)

            return round(
                math.degrees(val)
                if self.is_deg
                else val,
                12
            )


        def my_acos(x):

            val = math.acos(x)

            return round(
                math.degrees(val)
                if self.is_deg
                else val,
                12
            )


        def my_atan(x):

            val = math.atan(x)

            return round(
                math.degrees(val)
                if self.is_deg
                else val,
                12
            )


        # Ganti fungsi
        expr = expr.replace(
            'asin(',
            'my_asin('
        )

        expr = expr.replace(
            'acos(',
            'my_acos('
        )

        expr = expr.replace(
            'atan(',
            'my_atan('
        )

        expr = expr.replace(
            'sin(',
            'my_sin('
        )

        expr = expr.replace(
            'cos(',
            'my_cos('
        )

        expr = expr.replace(
            'tan(',
            'my_tan('
        )


        # =====================================================
        # KURUNG OTOMATIS
        # =====================================================

        open_b = expr.count('(')
        close_b = expr.count(')')


        if open_b > close_b:

            expr += ')' * (
                open_b - close_b
            )


        # =====================================================
        # EVALUASI
        # =====================================================

        allowed_globals = {

            'math': math,

            'my_sin': my_sin,
            'my_cos': my_cos,
            'my_tan': my_tan,

            'my_asin': my_asin,
            'my_acos': my_acos,
            'my_atan': my_atan

        }


        return eval(
            expr,
            allowed_globals
        )


    # =========================================================
    # TOMBOL KALKULATOR
    # =========================================================

    def on_button_click(self, instance):

        pressed_text = instance.text


        # AC
        if pressed_text == 'AC':

            self.formula = ''

            self.display.text = '0'


        # C
        elif pressed_text == 'C':

            self.formula = (
                self.formula[:-1]
            )

            self.display.text = (
                self.formula
                if self.formula
                else '0'
            )


        # =
        elif pressed_text == '=':

            try:

                res_val = self.evaluate_formula(
                    self.formula
                )


                if isinstance(
                    res_val,
                    float
                ):

                    if res_val.is_integer():

                        result = str(
                            int(res_val)
                        )

                    else:

                        result = (
                            f"{res_val:.10f}"
                            .rstrip('0')
                            .rstrip('.')
                        )

                else:

                    result = str(
                        res_val
                    )


                # Simpan history
                self.history_list.append(
                    f"{self.formula} = {result}"
                )


                self.display.text = result

                self.formula = result


            except Exception:

                self.display.text = 'Error'

                self.formula = ''


        # Tombol lainnya
        else:

            if self.display.text in [
                '0',
                'Error'
            ]:

                if pressed_text not in [
                    '.',
                    ',',
                    '+',
                    '-',
                    'x',
                    ':',
                    '%'
                ]:

                    self.formula = pressed_text

                else:

                    self.formula += pressed_text

            else:

                self.formula += pressed_text


            self.display.text = self.formula


# =========================================================
# APP
# =========================================================

class CalcApp(App):

    def build(self):

        return FixedCalculator()


# =========================================================
# RUN
# =========================================================

if __name__ == '__main__':

    CalcApp().run()