from logging import getLogger, LoggerAdapter
logger = getLogger(__name__)

import shutil
from itertools import cycle, repeat
from functools import reduce
from operator import add
from .viewabc import ViewABC
from kaleidoscope.color import ColoredText
from .attribute import AttributeRenderDatum

class ObjectView(ViewABC):
    """
    Description:
        Object Views are built up from a sequence of AttributeViews with delimiters.
    """
    def __init__(self, attribute_views, delimiters, prologue=None):
        """
        Input:
            attribute_views: list of AttributeView objects
            delimiter: ColoredText instance string used to separate AttributeViews when rendering
        """
        self.attribute_views = attribute_views
        self.delimiters = cycle(delimiters) if delimiters else repeat(ColoredText(''))
        self.prologue = prologue if prologue else ColoredText('')
        self.render_method = print

        self.term_size = shutil.get_terminal_size()


    def get_render_output(self, limit_to_screen=True):
        """
        Description:
            Get the output that will be passed to the render method. (the text that will
            be printed to a terminal)
        Input:
            limit_to_screen: boolean controlling whether or not we cut off the line at the
            line-length of the terminal
        """
        log = LoggerAdapter(logger, {'name_ext' : 'ObjectView.get_render_output'})

        #- figure out the width of each attribute view
        per_attr_widths = list()
        per_attr_colors = list()

        for n, attr_view in enumerate(self.attribute_views):
            attr_text = attr_view.get_render_data().attribute.plain()
            view_lines = attr_text.split('\n')
            if len(view_lines) <= 1:
                log.debug("single line attribute view")
                if n == 0:
                    log.debug(f"adding prologue length to attr_width: {attr_text}")
                    attr_width = len(attr_text) + len(self.prologue.plain())
                else:
                    log.debug(f"not adding prologue length to attr_width: {attr_text}")
                    attr_width = len(attr_text)
            else:
                log.debug("multi-line attribute view: ")
                log.debug("{}".format(view_lines))
                longest_line = max(*view_lines, key=len)
                attr_width = len(longest_line) + len(self.prologue.plain())
            log.debug("attr_width : {}".format(attr_width))
            per_attr_widths.append(attr_width)
            per_attr_colors.append(attr_view.color)
        log.debug("per_attr_widths: {}".format(per_attr_widths))

        #- build a list of lines to render for each attribute view
        #- one is just the text, so the length of the line is the
        #- length of the visible characters
        #- then we have the lines per attribute that also contain color code
        #- the text lines we use to determine the display length
        #- but the manipulation of the attribute view must
        #- be done on the lines to actually be rendered
        per_attr_text_lines = [[]] * len(self.attribute_views)
        per_attr_lines = [[]] * len(self.attribute_views)

        for n, attr_view in enumerate(self.attribute_views):
            attr_rd = attr_view.get_render_data()
            text_lines = attr_rd.attribute.plain().split('\n')
            #- first line has prologue
            if n == 0 and self.prologue:
                text_lines[0] = self.prologue.plain() + text_lines[0]

            per_attr_text_lines[n] = text_lines
            per_attr_lines[n] = [ColoredText(txt, attr_view.color) for txt in text_lines]

        #- figure out how many lines this object will take up
        if per_attr_text_lines:
            object_view_lines = len( max(*per_attr_text_lines, key=len))
        else:
            #- TODO: this assumes that we are always rendering attributes
            #- for builtins, that won't work
            object_view_lines = 0
            log.debug(f"no attributes to render")
        log.debug("{} lines in this object view".format(object_view_lines))

        #- combine the lists of attribute lines into a single list of object lines
        render_text_lines = list()
        render_lines = list()

        for line_num in range(object_view_lines):
            text_line = ''
            render_line = list()

            for m, attr_text_lines in enumerate(per_attr_text_lines):
                if len(attr_text_lines) > line_num:
                    log.debug(f"m: {m} | line_num: {line_num}")
                    log.debug(f"per_attr_widths[m]: {per_attr_widths[m]}")
                    log.debug(("len(attr_text_lines[line_num]):"
                            f"{len(attr_text_lines[line_num])}"))

                    pad_len = per_attr_widths[m] - len(attr_text_lines[line_num])

                    log.debug(f"initial pad_len: {pad_len}")

                    text_line += attr_text_lines[line_num]
                    text_line += ' ' * pad_len
                    cur_render_line = per_attr_lines[m][line_num]

                    log.debug("cur_text_line initial:")
                    log.debug(f"'{attr_text_lines[line_num]}'")
                    log.debug("cur_render_line initial: ")
                    log.debug(f"'{cur_render_line}'")

                    cur_render_line.text += ' ' * pad_len

                    log.debug("cur_render_line plus padding: ")
                    log.debug(f"'{cur_render_line}'")

                    render_line.append(cur_render_line)

                    if m < len(per_attr_text_lines) - 1:
                        delim = next(self.delimiters)
                        text_line += delim.plain()
                        render_line.append(delim)
                        log.debug("render_line plus pad and delim:")
                        log.debug("{}".format(render_line))
                else:
                    log.debug("adding padded stanza line")
                    text_line += ' ' * per_attr_widths[m]
                    log.debug("padded text line: ")
                    log.debug(f"'{text_line}'")
                    #- all attribute lines should have the same color for now
                    color = per_attr_lines[m][0].color
                    render_line.append(ColoredText(' ' * per_attr_widths[m], color))
                    log.debug("padded render line: ")
                    log.debug("'{render_line}'")

                    if m < len(per_attr_text_lines) - 1:
                        delim = next(self.delimiters)
                        text_line += delim.plain()
                        render_line.append(delim)
                        log.debug("padded render_line plus delim:")
                        log.debug(f"{render_line}")

            render_text_lines.append(text_line)
            log.debug('rendered render_line:')
            log.debug(''.join([x.render() for x in render_line]))
            render_lines.append(render_line)


        if limit_to_screen:
            #- trim plaintext to fit screen width
            log.debug("screen size: {}".format(self.term_size.columns))
            for n, line in enumerate(render_text_lines[:]):
                if len(line) > self.term_size.columns:
                    length = len(line)
                    log.debug("trimming line #{} to fit screen (len={})".format(n, length))
                    render_text_lines[n] = line[0:self.term_size.columns] 

            #- trim colored text to fit screen width
            for n, render_line in enumerate(render_lines[:]):
                running_text_width = 0
                for m, item in enumerate(render_line[:]):
                    current_text_width = running_text_width
                    log.debug("current text width: {}".format(current_text_width))
                    running_text_width += len(item.plain())
                    if running_text_width > self.term_size.columns:
                        log.debug("detected overrun at {}-->{}".format(\
                            running_text_width, current_text_width))
                        log.debug("overrun item: {}".format(item))
                        extra = running_text_width - self.term_size.columns
                        item.text = item.text[0:-extra]
                        log.debug("trimmed item: {}".format(item))
                        render_line[m] = item
                        render_lines[n] = render_line

        render_output = ''
        for n, render_line in enumerate(render_lines):
            for item in render_line:
                render_output += item.render()
            if n < len(render_lines) - 1:
                render_output += '\n'

        return render_output
        #debug: return just the plain text
        #return '\n'.join(render_text_lines)

        
    def render(self):
        """
        Description:
            Render the Object View on the output device. (print text on a terminal.)
        """
        self.render_method(self.get_render_output())
