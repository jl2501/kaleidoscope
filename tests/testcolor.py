"""Test the render.color module"""
import unittest
from kaleidoscope.color import Color, TerminalColorCodes, ColoredText

class TestColorClass(unittest.TestCase):
    def test_init_tcc(self):
        tcc = TerminalColorCodes()
        self.assertEqual(tcc.data, TerminalColorCodes.get_default_colors())

    def test_init_color(self):
        color = Color('bright green on black')
        self.assertEqual(color.foreground, 'green')
        self.assertEqual(color.style, 'bright')
        self.assertEqual(color.background, 'black')
        
        color = Color('red on black')
        self.assertEqual(color.foreground, 'red')
        self.assertEqual(color.style, 'normal')
        self.assertEqual(color.background, 'black')

        color = Color('red on yellow')
        self.assertEqual(color.foreground, 'red')
        self.assertEqual(color.style, 'normal')
        self.assertEqual(color.background, 'yellow')

        color = Color('cyan')
        self.assertEqual(color.foreground, 'cyan')
        self.assertEqual(color.style, 'normal')
        self.assertEqual(color.background, 'black')

    def test_printed_color(self):
        color = Color('bright cyan on black')
        text = '[bright cyan on black test text blob]'
        colored_text = color.terminal_codes() + text + color.terminal_reset
        self.assertEqual(colored_text, '\x1b[36m\x1b[40m\x1b[1m[bright cyan on black test text blob]\x1b[0m')
        print(colored_text)


    def test_color_name(self):
        color = Color('bright red on white')
        self.assertEqual(color.get_color_name(), 'bright red on white')
        color = Color('white on cyan')
        self.assertEqual('normal white on cyan', color.get_color_name())
        color = Color('magenta')
        self.assertEqual('normal magenta on black', color.get_color_name())




class TestColoredText(unittest.TestCase):
    def test_init(self):
        ct = ColoredText(text='Hello World!', color='bright white on green')
        self.assertEqual(ct.to_str(), '\x1b[37m\x1b[42m\x1b[1mHello World!\x1b[0m')


if __name__ == '__main__':
    unittest.main()
