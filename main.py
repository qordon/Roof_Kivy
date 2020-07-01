from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.config import Config
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore

Config.set('kivy', 'keyboard_mode', 'systemanddock')

kv = '''
<ItemLabel@Label>:
    font_size: '24sp'
    halign: 'left'
    valign: 'middle'
    text_size: self.size

<ItemTextInput@TextInput>:
    text: '0'
    font_size: '19sp'

<MenuScreen>:
    choice_type: choice_type
    btn_settings: btn_settings
    adress: adress
    
    square_meters: square_meters
    perimeter: perimeter
    add_corners: add_corners
    lamp: lamp
    soffit: soffit 
    
    output: output
    
    
    BoxLayout:
        canvas.before:
            Color:
                rgba: 34/255, 36/255, 39/255, 1
            Rectangle:
                pos: self.pos
                size: self.size
    
        orientation: 'vertical'
        padding: 10
        spacing: 20
        
        BoxLayout:
            size_hint: [1, 0.4]
            padding: [5, 10, 0,10]
            spacing: 5
            Spinner:
                id: choice_type
                text: 'Вид плёнки'
                font_size: '24sp'
                values: ('Глянец, мат, сатин', 'Фактурная')
                values_size: 50
            Button:
                id: btn_settings
                ##text: 'Настройки'
                size_hint: [0.24, 1]
                on_press:
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'settings'
                Image:
                    source: 'settings.png'
                    size: self.parent.width - 10, self.parent.height - 10                    
                    pos: self.parent.x + 5, self.parent.y + 5
        
        BoxLayout:
            size_hint: [1, 0.2]
            padding: [5, 0, 0, 0]
            ItemTextInput:
                id: adress
                text: ''
        
        GridLayout:
            cols: 2
            spacing: 30
            BoxLayout:
                orientation: 'vertical'
                ItemLabel:
                    id: sign_square_meters
                    text: ' Кол-во кв. м.'
                ItemLabel:
                    id: sign_perimeter
                    text: ' Периметр'
                ItemLabel:
                    id: sign_add_corners
                    text: ' Дополнительные углы'
                ItemLabel:
                    id: sign_lamp
                    text: ' Центральный светильник'
                    font_size: '21sp'
                ItemLabel:
                    id: sign_soffit
                    text: ' Соффиты'
            BoxLayout:
                orientation: 'vertical'
                size_hint: [0.25, 1]
                ItemTextInput:
                    id: square_meters
    
                ItemTextInput:
                    id: perimeter
    
                ItemTextInput:
                    id: add_corners
    
                ItemTextInput:
                    id: lamp
    
                ItemTextInput:
                    id: soffit
        
        BoxLayout:
            size_hint: [1, 0.3]
            padding: [60, 0, 60, 0]
    
            Button:
                text: 'Рассчитать'
                font_size: '30sp'
                on_release:
                    root.calculate()
       
        Label:
            id: output
            text: 'Информация'
            font_size: '36sp'
            size_hint: [1, 0.6]
            halign: 'center'
            valign: 'middle'
            text_size: self.size
    
        BoxLayout:
            size_hint: [1, 0.2]
            padding: [50, 0, 50, 0]
            Button:
                text: 'Очистить'
                font_size: '24sp'
                on_release:
                    root.clear()
        
                    
<SettingsScreen>:
    price_normal: price_normal
    price_textured: price_textured
    price_perimeter: price_perimeter
    price_corners: price_corners
    price_lamp: price_lamp
    price_soffit: price_soffit
    output_settings: output_settings
    
    BoxLayout:
        padding: [0, 10, 10, 0]
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 34/255, 36/255, 39/255, 1
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            size_hint: [0.4, 0.15]
            padding: [10, 10, 50, 5]
            Button:
                text: 'Назад'
                font_size: '24sp'
                on_press:
                    output_settings.text = ' '
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'menu'
                    
        Label:
            text: 'Цена'
            font_size: '36sp'
            size_hint: [1, 0.1] 
                
        GridLayout:
            cols: 2
            spacing: 30
            size_hint: [1, 0.5]
            BoxLayout:
                size_hint: [1, 0.5]
                orientation: 'vertical'
                ItemLabel:
                    text: ' Глянец, мат, сатин'
                ItemLabel:
                    text: ' Фактурная'
                ItemLabel:
                    text: ' Периметр'
                ItemLabel:
                    text: ' Дополнительные углы'
                ItemLabel:
                    text: ' Центральный светильник'
                    font_size: '21sp'
                ItemLabel:
                    text: ' Соффиты'
            BoxLayout:
                size_hint: [1, 0.5]
                orientation: 'vertical'
                size_hint: [0.25, 1]
                ItemTextInput:
                    id: price_normal
                    text: '400'
                ItemTextInput:
                    id: price_textured
                    text: '600'
                ItemTextInput:
                    id: price_perimeter
                    text: '25'
                ItemTextInput:
                    id: price_corners
                    text: '80'
                ItemTextInput:
                    id: price_lamp
                    text: '200'
                ItemTextInput:
                    id: price_soffit
                    text: '220'
    
        BoxLayout:
            padding: [50, 30, 50, 70]
            size_hint: [1, 0.3]
            Button:
                text: 'Сохранить'
                font_size: '24sp'
                on_press:
                    root.save_price([price_normal.text, price_textured.text, price_perimeter.text, \
                    price_corners.text, price_lamp.text, price_soffit.text])
                
        Label:
            id: output_settings
            size_hint: [1, 0.2]
            font_size: '28sp'
            halign: 'center'
            valign: 'top'
            text_size: self.size    
'''
Builder.load_string(kv)

Window.size = (390, 630)

class MenuScreen(Screen):
    price = []
    stored_data = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stored_data = JsonStore('info.json')

        if self.stored_data.exists('mydata'):
            self.price = self.stored_data.get('mydata')['text']
            self.price = [float(i) for i in self.price]
        else:
            temp = ['400', '600', '25', '80', '200', '220']
            self.stored_data.put('mydata', text=temp)
            self.price = [float(i) for i in temp]

    def clear(self):
        self.choice_type.text = 'Вид плёнки'
        self.adress.text = ''
        self.square_meters.text = '0'
        self.perimeter.text = '0'
        self.add_corners.text = '0'
        self.lamp.text = '0'
        self.soffit.text = '0'
        self.output.text = 'Информация'
        self.output.font_size = '36sp'

    def calculate(self):
        result = 0.0
        try:
            if self.choice_type.text == 'Фактурная':
                type_skin = self.price[1]
            elif self.choice_type.text == 'Глянец, мат, сатин':
                type_skin = self.price[0]

            if float(self.square_meters.text) < 0:
                raise Exception()
            elif float(self.square_meters.text) < 15:
                result += ((15 - float(self.square_meters.text)) * 10 + type_skin) * float(self.square_meters.text)
            else:
                result += float(self.square_meters.text) * type_skin



            if float(self.perimeter.text) < 0 or float(self.lamp.text) < 0 \
                    or float(self.soffit.text) < 0 or float(self.add_corners.text) < 0:
                raise Exception()

            result += float(self.perimeter.text) * self.price[2]
            result += float(self.add_corners.text) * self.price[3]
            result += float(self.lamp.text) * self.price[4]
            result += float(self.soffit.text) * self.price[5]

            if result.is_integer():
                result = int(result)

            self.output.text = "Итого:\n" + str(round(result, 2)) + " руб"
            self.output.font_size = '36sp'
        except:
            self.output.text = "Неверный ввод данных"

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            temp = sm.get_screen('menu').stored_data.get('mydata')['text']

            self.price_normal.text = temp[0]
            self.price_textured.text = temp[1]
            self.price_perimeter.text = temp[2]
            self.price_corners.text = temp[3]
            self.price_lamp.text = temp[4]
            self.price_soffit.text = temp[5]
        except:

            temp = [self.price_normal.text,
                    self.price_textured.text,
                    self.price_perimeter.text,
                    self.price_corners.text,
                    self.price_lamp.text,
                    self.price_soffit.text]

            sm.get_screen('menu').stored_data.put('mydata', text=temp)


    def save_price(self, cost):
        sm.get_screen('menu').price.clear()
        try:
            for i in range(len(cost)):
                sm.get_screen('menu').price.append(round(float(cost[i]), 2))
            sm.get_screen('menu').stored_data.put('mydata', text=cost)
            self.output_settings.text = 'Сохранено'
        except:
            self.output_settings.text = 'Данные введены неверно'
            self.output_settings.font_size = '28sp'


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))


class RoofApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    RoofApp().run()

