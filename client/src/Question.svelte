<script>
  import { useMutation, useQueryClient } from '@sveltestack/svelte-query'
  import marked from 'marked'
  import DOMPurify from 'dompurify'

  export let text
  export let creator
  export let created
  export let votes
  export let id
  export let closed

  $: createDate = new Date(created)
  $: votedFor = (votes.indexOf(jhdata.user) > -1)

  const queryClient = useQueryClient()
  const voteMutation = useMutation(async (vote) => {
    const url = `${jhdata.prefix}vote/${id}/${vote}`
    const response = await fetch(url, {method: 'POST'})
    if (!response.ok) {
      throw new Error('Failure to update vote')
    }
    // Don't worry about syncing state on votes.
  })
  const closeMutation = useMutation(async (which) => {
    const url = `${jhdata.prefix}${which}/${id}`
    const response = await fetch(url, {method: 'POST'})
    if (!response.ok) {
      throw new Error('Failure to change closed status')
    }
    // Don't worry about syncing state on closes.
  })

  function toggleVote() {
    $voteMutation.mutate(votedFor ? '-' : '+')
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
    $closeMutation.mutate(closed ? 'open': 'close')
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
    <button class="close" class:closed on:click={toggleClose}
            title={closed ? "Re-open" : "Close"}>
      {closed ? '⟲' : '✖'}
    </button>
  {/if}
  <div class="votes">
    <button class="upvote" class:votedFor on:click={toggleVote}>👍</button>
    <div class="count">+{votes.length}</div>
  </div>
  <div class="text">{@html DOMPurify.sanitize(marked(text))}</div>
  <div class="meta">
    Asked by {creator.split('@')[0]} on {createDate.toDateString()}.
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

  div.text > :global(:first-child) {
    margin-top: 0;
  }
  div.text > :global(:last-child) {
    margin-bottom: 0;
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
