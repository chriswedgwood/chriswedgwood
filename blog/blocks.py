from wagtail.wagtailcore import blocks

CODE_CHOICES = [
    ('python', 'python'),
    ('javascript', 'javascript'),
    ('css', 'css'),
    ('markup', 'markup')
]


class CodeBlock(blocks.StructBlock):
    language = blocks.ChoiceBlock(choices=CODE_CHOICES, default="python")
    text = blocks.TextBlock()

    class Meta:
        template = "code_section.html"
        icon = "openquote"
        label = "Code Block"

