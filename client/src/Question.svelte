<script>
  export let text
  export let creator
  export let created
  export let votes
  export let id
  export let closed

  $: createDate = new Date(created)
</script>

<div class="question">
  <div class="votes">
    <button class="upvote">+1</button>
    <div class="count">+{votes.length}</div>
  </div>
  <div class="text">{text}</div>
  <div class="meta">
    Asked by {creator} on {createDate.toDateString()}.
  </div>
</div>

<style>
  div.question {
    margin: 1em;
    border: thin solid #ddd;
    border-radius: 0.5em;
    padding: 1em;
    background-color: white;
  }

  div.votes {
    float: right;
    text-align: center;
    padding-left: 0.5em;
    background-color: white;
  }

  div.meta {
    margin-top: 0.5em;
    border-top: thin solid #eee;
    padding-top: 0.5em;
  }

  div.meta, div.count {
    font-size: small;
    color: #999;
  }
</style>
