---
layout: default
title: Home
---

# home page
page title: {{ page.title | upcase}}

page url: {{ "/" | absolute_url | upcase}}

site title: {{ site.title }}

site time: {{ site.time | date_to_xmlschema }}