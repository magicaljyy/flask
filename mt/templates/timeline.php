{% extends "base.html" %}
{% block title %}
  {% if request.endpoint == 'public_timeline' %}
    Public Timeline
  {% elif request.endpoint == 'user_timeline' %}
    {{ profile_user.username }}'s Timeline
  {% else %}
    My Timeline
  {% endif %}
{% endblock %}
{% block body %}
  <h2>{{ self.title() }}</h2>
  {% if g.user %}
    {% if request.endpoint == 'user_timeline' %}
      <div class="followstatus">
      {% if g.user.user_id == profile_user.user_id %}
        This is you!
      {% elif followed %}
        You are currently following this user.
        <a class="unfollow" href="{{ url_for('unfollow_user', username=profile_user.last_name)
          }}">Unfollow user</a>.
      {% else %}
        You are not yet following this user.
        <a class="follow" href="{{ url_for('follow_user', username=profile_user.last_name)
          }}">Follow user</a>.
      {% endif %}
      </div>
    {% elif request.endpoint == 'timeline' %}
      <div class="twitbox">
        <h3>What's on your mind {{ g.user.username }}?</h3>
        <form action="{{ url_for('add_message') }}" method="post">
          <p><input type="text" name="text" size="60"><!--
          --><input type="submit" value="Share">
        </form>
      </div>
    {% endif %}
  {% endif %}
  <ul class="messages">
  {% for message in messages %}
    <li><img src="{{ message.email|gravatar(size=48) }}"><p>
      <strong><a href="{{ url_for('user_timeline', username=message.last_name)
      }}">{{ message.username }}</a></strong>
      {{ message.text }}
      <small>&mdash; {{ message.pub_date|datetimeformat }}</small>
  {% else %}
    <li><em>There's no message so far.</em>
  {% endfor %}
  </ul>
{% endblock %}