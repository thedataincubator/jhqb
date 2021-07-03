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
  const mutation = useMutation(async (vote) => {
    const url = `http://localhost:8000/vote/${id}/${vote}`
    const response = await fetch(url, {
      method: 'POST'
    })
    if (!response.ok) {
      throw new Error('Failure to update vote')
    }
    // Don't worry about syncing state on votes.
  })

  function toggleVote() {
    $mutation.mutate(votedFor ? '-' : '+')
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
</script>

<div class="question" id="{id}">
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
