---
id: 719    

permalink: /pmlogy-tags
title: "PMLOGY Tag - Posts"
author_profile: true
toc: true
toc_sticky: true
header:
  image: "../assets/images/banners/pmblog-Banner.jpg"
sidebar:
   nav: "docs"
---

## Welcome to dasarpAI Project Management Blog - Posts!

{% include group-by-array collection=site.pmblog field="tags" %}

{% for tag in group_names %}
{% assign posts = group_items[forloop.index0] %}

  <h1 id="{{ tag | slugify }}" class="archive__subtitle">{{ tag }}</h1>
  {% for post in posts %}
    {% include archive-single.html %}
  {% endfor %}
{% endfor %}

{% include group-by-array collection=site.pmbok6 field="tags" %}

{% for tag in group_names %}
{% assign posts = group_items[forloop.index0] %}

  <h1 id="{{ tag | slugify }}" class="archive__subtitle">{{ tag }}</h1>
  {% for post in posts %}
    {% include archive-single.html %}
  {% endfor %}
{% endfor %}

{% include group-by-array collection=site.pmbok6hi field="tags" %}

{% for tag in group_names %}
{% assign posts = group_items[forloop.index0] %}

  <h1 id="{{ tag | slugify }}" class="archive__subtitle">{{ tag }}</h1>
  {% for post in posts %}
    {% include archive-single.html %}
  {% endfor %}
{% endfor %}

