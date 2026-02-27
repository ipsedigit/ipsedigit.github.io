---
layout: page
title: "Android Dev Hub"
description: "Trending Android repositories and curated news for Android developers. Kotlin, Jetpack Compose, and the Android ecosystem — updated daily."
permalink: /android/
---

{% assign repos = site.data.android.repos %}
{% assign articles = site.data.android.articles %}

<div style="display:flex; gap:1em; flex-wrap:wrap; margin-bottom:1.5em;">
  <a href="#trending-repos" style="padding:4px 12px; border-radius:12px; background:#dbeafe; color:#1e40af; font-weight:bold; text-decoration:none; cursor:pointer;">Repos: {{ repos.size }}</a>
  <a href="#android-news" style="padding:4px 12px; border-radius:12px; background:#dcfce7; color:#166534; font-weight:bold; text-decoration:none; cursor:pointer;">Articles: {{ articles.size }}</a>
  <span style="padding:4px 12px; border-radius:12px; background:#fef3c7; color:#92400e; font-weight:bold;">Top Language: Kotlin</span>
</div>

## 📱 Repo of the Day

<div style="margin-bottom:1.5em; padding:1em; border:2px solid #a855f7; border-radius:12px; background:#faf5ff;">
  <div style="display:flex; align-items:center; gap:0.5em; margin-bottom:0.5em; flex-wrap:wrap;">
    <img src="https://avatars.githubusercontent.com/u/31833384?v=4&s=32" alt="" width="32" height="32" style="border-radius:50%;">
    <strong style="font-size:1.2em;"><a href="https://github.com/2dust/v2rayNG" target="_blank" rel="noopener">2dust/v2rayNG</a></strong>
    <a href="https://github.com/2dust/v2rayNG" target="_blank" rel="noopener" style="padding:2px 8px; border-radius:12px; font-size:0.8em; background:#a855f7; color:#fff; text-decoration:none;">⭐ Repo of the Day</a>
    <span style="font-size:0.85em; color:#7e22ce;">0 stars today</span>
  </div>
  <p style="margin:0.3em 0; color:#374151;">A V2Ray client for Android, support Xray core and v2fly core</p>
  <div style="display:flex; gap:1em; font-size:0.85em; color:#6b7280; flex-wrap:wrap;">
    <span>&#9733; 51,458</span>
    <span>&#127860; 6,978</span>
    <span>Kotlin</span>
    <span>GPL-3.0</span>
  </div>
  <div style="margin-top:0.5em;"><a href="/tags/android/" style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#f3e8ff; border-radius:6px; color:#7e22ce; font-size:0.75em; text-decoration:none;">android</a> <a href="/tags/proxy/" style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#f3e8ff; border-radius:6px; color:#7e22ce; font-size:0.75em; text-decoration:none;">proxy</a> <a href="/tags/shadowsocks/" style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#f3e8ff; border-radius:6px; color:#7e22ce; font-size:0.75em; text-decoration:none;">shadowsocks</a> <a href="/tags/socks5/" style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#f3e8ff; border-radius:6px; color:#7e22ce; font-size:0.75em; text-decoration:none;">socks5</a> <a href="/tags/trojan/" style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#f3e8ff; border-radius:6px; color:#7e22ce; font-size:0.75em; text-decoration:none;">trojan</a> <a href="/tags/v2fly/" style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#f3e8ff; border-radius:6px; color:#7e22ce; font-size:0.75em; text-decoration:none;">v2fly</a> <a href="/tags/v2ray/" style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#f3e8ff; border-radius:6px; color:#7e22ce; font-size:0.75em; text-decoration:none;">v2ray</a> <a href="/tags/vless/" style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#f3e8ff; border-radius:6px; color:#7e22ce; font-size:0.75em; text-decoration:none;">vless</a></div>
</div>

## Charts

<div style="display:flex; gap:2em; flex-wrap:wrap; margin-bottom:2em;">
  <div style="flex:1; min-width:280px; max-width:400px;">
    <h3 style="font-size:1rem; margin-bottom:0.5rem;">Language Distribution</h3>
    <canvas id="langChart" width="380" height="380"></canvas>
  </div>
  <div style="flex:2; min-width:300px;">
    <h3 style="font-size:1rem; margin-bottom:0.5rem;">Top Repos by Stars</h3>
    <canvas id="starsChart" width="600" height="380"></canvas>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
<script>
new Chart(document.getElementById('langChart'), {
  type: 'doughnut',
  data: {
    labels: ["Kotlin"],
    datasets: [{ data: [25], backgroundColor: ["#A97BFF"] }]
  },
  options: { responsive: true, plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, padding: 8, font: { size: 11 } } } } }
});
new Chart(document.getElementById('starsChart'), {
  type: 'bar',
  data: {
    labels: ["v2rayNG", "okhttp", "architecture-samples", "shadowsocks-android", "gkd", "leakcanary", "librepods", "Seal", "SmsForwarder", "BaseRecyclerViewAdap"],
    datasets: [{ label: 'Stars', data: [51458, 46905, 45585, 36659, 36338, 29900, 25571, 24830, 24687, 24622], backgroundColor: '#a855f7', borderRadius: 4 }]
  },
  options: {
    indexAxis: 'y', responsive: true,
    plugins: { legend: { display: false } },
    scales: { x: { ticks: { callback: function(v) { return v >= 1000 ? (v/1000).toFixed(0) + 'k' : v; } } } }
  }
});
</script>

## Latest Android News {#android-news}

{% for article in articles %}
<div style="margin-bottom:1em; padding:0.75em; border:1px solid #e5e7eb; border-radius:8px;">
  <strong><a href="{{ article.url }}" target="_blank" rel="noopener">{{ article.title }}</a></strong>
  <p style="margin:0.25em 0; font-size:0.88em; color:#374151;">{{ article.excerpt }}</p>
  <span style="font-size:0.78em; color:#9ca3af;">{{ article.source }} &middot; {{ article.published | slice: 0, 10 }}</span>
</div>
{% endfor %}

## Trending Android Repos {#trending-repos}

{% for repo in repos %}
<div style="margin-bottom:1.2em; padding:0.75em; border:1px solid #e5e7eb; border-radius:8px;">
  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap;">
    <img src="{{ repo.owner_avatar }}&s=24" alt="" width="24" height="24" style="border-radius:50%;" loading="lazy">
    <strong><a href="{{ repo.repo_url }}" target="_blank" rel="noopener">{{ repo.name }}</a></strong>
    {% if repo.language %}
      {% assign lang_slug = repo.language | slugify %}
      <a href="/tags/{{ lang_slug }}/" style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; text-decoration:none; background:{% if repo.language == 'Kotlin' %}#A97BFF{% elsif repo.language == 'Java' %}#b07219{% elsif repo.language == 'C++' %}#f34b7d{% elsif repo.language == 'Dart' %}#00B4AB{% elsif repo.language == 'Swift' %}#F05138{% else %}#6b7280{% endif %};">{{ repo.language }}</a>
    {% endif %}
    {% if repo.badge == "new_entry" %}
      <a href="{{ repo.repo_url }}" target="_blank" rel="noopener" style="padding:2px 8px; border-radius:12px; font-size:0.75em; text-decoration:none; background:#dbeafe; color:#1e40af; font-weight:bold;">🆕 NEW</a>
    {% elsif repo.badge == "rising" %}
      <a href="{{ repo.repo_url }}" target="_blank" rel="noopener" style="padding:2px 8px; border-radius:12px; font-size:0.75em; text-decoration:none; background:#dcfce7; color:#166534; font-weight:bold;">📈 +{{ repo.star_delta }}</a>
    {% elsif repo.badge == "cooling" %}
      <a href="{{ repo.repo_url }}" target="_blank" rel="noopener" style="padding:2px 8px; border-radius:12px; font-size:0.75em; text-decoration:none; background:#fee2e2; color:#991b1b; font-weight:bold;">📉 {{ repo.star_delta }}</a>
    {% endif %}
  </div>
  <p style="margin:0.3em 0; font-size:0.9em; color:#374151;">{{ repo.description }}</p>
  <span style="font-size:0.85em; color:#6b7280;">
    &#9733; {{ repo.stars }}
    &middot; &#127860; {{ repo.forks }}
    &middot; Updated: {{ repo.last_push | date: '%b %d, %Y' }}
    {% if repo.star_delta != 0 %}&middot; <span style="color:{% if repo.star_delta > 0 %}#16a34a{% else %}#dc2626{% endif %};">{% if repo.star_delta > 0 %}+{% endif %}{{ repo.star_delta }} today</span>{% endif %}
  </span>
  {% if repo.topics.size > 0 %}
  <br><span style="font-size:0.75em;">
    {% for topic in repo.topics %}
      {% assign topic_slug = topic | slugify %}<a href="/tags/{{ topic_slug }}/" style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#f3f4f6; border-radius:6px; color:#374151; text-decoration:none;">{{ topic }}</a>
    {% endfor %}
  </span>
  {% endif %}
</div>
{% endfor %}

---

<p style="font-size:0.8em; color:#9ca3af;">
Data from <a href="https://github.com">GitHub</a> Search API &amp; RSS feeds &middot; Updated: {{ site.data.android.generated_at }}
</p>
