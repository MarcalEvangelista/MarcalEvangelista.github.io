---
title: "Publications"
permalink: /publications/
layout: single
author_profile: true
---

{% for pub in site.data.publications %}
- **[{{ pub.title }}]({{ pub.url }})**  
  <small>{{ pub.authors }} — {{ pub.year }}</small>
{% endfor %}

