<script>
  import { useMutation, useQueryClient } from '@sveltestack/svelte-query'
  export let text
  export let creator
  export let created
  export let votes
  export let id
  export let closed

  $: createDate = new Date(created)
  $: votedFor = (votes.indexOf(jhdata.user) > -1)

  const queryClient = useQueryClient()
  // These objects appear to be reused, and the mutations don't get
  // regenerated as the id changes.  Therefore, we need to be sure to
  // pass the id in as an argument, so that we get the current id, not
  // the id from when the object was first created.
  const voteMutation = useMutation(async ({ vote, id }) => {
    const url = `http://localhost:8000/vote/${id}/${vote}`
    const response = await fetch(url, {method: 'POST'})
    if (!response.ok) {
      throw new Error('Failure to update vote')
    }
    // Don't worry about syncing state on votes.
  })
  const closeMutation = useMutation(async ({ which, id }) => {
    const url = `http://localhost:8000/${which}/${id}`
    const response = await fetch(url, {method: 'POST'})
    if (!response.ok) {
      throw new Error('Failure to change closed status')
    }
    // Don't worry about syncing state on closes.
  })

  function toggleVote() {
    $voteMutation.mutate({vote: votedFor ? '-' : '+', id: id})
    queryClient.setQueryData('questions', (data) => {
      for (let question of data) {
        if (question.id === id) {
          if (!votedFor) {
            question.votes.push(jhdata.user)
          } else {
            question.votes = question.votes.filter(u => u !== jhdata.user)
          }
        }
      }
      return data
    })
  }

  function toggleClose() {
    $closeMutation.mutate({which: closed ? 'open': 'close', id: id})
    queryClient.setQueryData('questions', (data) => {
      for (let question of data) {
        if (question.id === id) {
          question.closed = !closed
        }
      }
      return data
    })
  }
</script>

<div class="question" id="{id}">
  {#if jhdata['user'] === creator || jhdata['admin_access']}
    <button class="close" class:closed on:click={toggleClose}>
      {closed ? '⟲' : '✖'}
    </button>
  {/if}
  <div class="votes">
    <button class="upvote" class:votedFor on:click={toggleVote}>👍</button>
    <div class="count">+{votes.length}</div>
  </div>
  <div class="text">{text}</div>
  <div class="meta">
    Asked by {creator} on {createDate.toDateString()}.
  </div>
</div>

<style>
  div.question {
    position: relative;
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

  button.upvote {
    border-radius: 100%;
    background-color: #def;
    filter: grayscale(1.0);
    cursor: pointer;
  }
  button.upvote:hover, button.upvote.votedFor {
    filter: grayscale(0.0);
  }
  button.upvote:hover {
    border-color: #9cf;
  }

  button.close {
    display: none;
    position: absolute;
    right: -0.5em;
    top: -0.5em;
    width: 1.5em;
    height: 1.5em;
    border-radius: 100%;
    background-color: #f66;
    color: white;
    cursor: pointer;
    justify-content: center;
    align-items: center;
  }
  button.close.closed {
    background-color: #6c6;
  }
  div.question:hover button.close {
    display: flex;
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
