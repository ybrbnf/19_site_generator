from jinja2 import Template
from markdown import markdown
import json
from os import path, makedirs


TEMPLATES_DIR = 'templates'
OUTPUT_DIR = 'output'


def load_config(filepath):
    with open(filepath, 'r') as config:
        return json.load(config)


def create_dir(directory):
    if not path.exists(directory):
        makedirs(directory)


def get_index_page(config):
    template = get_template('index.html')
    for article in config['articles']:
        article['article_url'] = get_article_url(article['source'])
    output_filepath = '{0}/{1}'.format(OUTPUT_DIR, 'index.html')
    render_page(config, output_filepath, template)


def get_article_page(config):
    template = get_template('article.html')
    for article in config['articles']:
        article_info = {'title': article['title'],
                        'text': convert_md_to_html(article['source']),
                        }
        filepath = path.dirname(article['source'])
        article_url = get_article_url(article['source'])
        output_dir = '{0}/{1}'.format(OUTPUT_DIR, filepath)
        create_dir(output_dir)
        render_page(article_info, article_url, template)


def get_article_url(source):
    source = path.splitext(source)[0].replace(' ', '_')
    output_source = '{0}/{1}.{2}'.format(OUTPUT_DIR, source, 'html')
    return output_source


def get_template(template_name):
    template_filepath = '{0}/{1}'.format(TEMPLATES_DIR, template_name)
    pattern = open(template_filepath).read()
    template = Template(pattern)
    return template


def render_page(data, filepath, template):
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(template.render(info=data))


def convert_md_to_html(filepath):
    filepath = '{0}/{1}'.format('articles', filepath)
    with open(filepath, 'r', encoding='utf-8') as data:
        return markdown(data.read(), extensions=['codehilite', 'fenced_code'])


if __name__ == '__main__':
    config = load_config('config.json')
    create_dir(OUTPUT_DIR)
    get_index_page(config)
    get_article_page(config)
