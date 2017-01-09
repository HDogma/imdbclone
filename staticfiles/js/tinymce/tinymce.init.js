tinymce.init({
    selector: 'textarea',
    browser_spellcheck: true,
    style_formats: [
    {title: 'Inline', items: [
      {title: 'Bold', icon: 'bold', format: 'bold'},
      {title: 'Italic', icon: 'italic', format: 'italic'},
      {title: 'Underline', icon: 'underline', format: 'underline'},
      {title: 'Strikethrough', icon: 'strikethrough', format: 'strikethrough'},
      {title: 'Superscript', icon: 'superscript', format: 'superscript'},
      {title: 'Subscript', icon: 'subscript', format: 'subscript'},
      {title: 'Code', icon: 'code', format: 'code'}
    ]},
    {title: 'Blocks', items: [
      {title: 'Paragraph', format: 'p'},
      {title: 'Blockquote', format: 'blockquote'},
      {title: 'Div', format: 'div'},
      {title: 'Pre', format: 'pre'}
    ]},
    {title: 'Alignment', items: [
      {title: 'Left', icon: 'alignleft', format: 'alignleft'},
      {title: 'Center', icon: 'aligncenter', format: 'aligncenter'},
      {title: 'Right', icon: 'alignright', format: 'alignright'},
      {title: 'Justify', icon: 'alignjustify', format: 'alignjustify'}
    ]}
  ]
  });/**
 * Created by h_dogma on 18.10.16.
 */
