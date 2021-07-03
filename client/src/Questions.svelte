<script>
  import { afterUpdate } from 'svelte'
  import { useQuery } from '@sveltestack/svelte-query'
  import Question from './Question.svelte'
  import Ask from './Ask.svelte'

  async function fetchQuestions() {
    const response = await fetch('http://localhost:8000/questions')
    if (!response.ok) {
      throw new Error('Failure to fetch questions')
    }
    return await response.json()
  }

  let scrollId = null
  let sortVal = 'date'
  let sortDir = +1
  const queryResult = useQuery('questions', fetchQuestions)

  // Mark as reactive so sort is recalculated when variables change
  $: sortQuestions = (a, b) => {
    let diff = (sortVal === 'date'
                ? new Date(a.created) - new Date(b.created)
                : a.votes.length - b.votes.length)
    return sortDir * diff
  }

  afterUpdate(() => {
    if (scrollId !== null) {
      // It can take several updates before the element shows up....
      let element = document.getElementById(scrollId)
      if (element !== null) {
        document.getElementById(scrollId).scrollIntoView()
        scrollId = null
      }
    }
  })
</script>

<div class="options">
  <span class="sort">
    Sort by
    <button
      on:click={() => {
        if (sortVal !== 'date') {
          sortVal = 'date'
          sortDir = +1
        } else {
          sortDir = -sortDir
        }
      }}
      class:sortUp={sortVal === 'date' && sortDir === 1}
      class:sortDown={sortVal === 'date' && sortDir === -1}
    >Date</button>
    <button
      on:click={() => {
        if (sortVal !== 'votes') {
          sortVal = 'votes'
          sortDir = -1
        } else {
          sortDir = -sortDir
        }
      }}
      class:sortUp={sortVal === 'votes' && sortDir === 1}
      class:sortDown={sortVal === 'votes' && sortDir === -1}
    >Votes</button>
  </span>
</div>
<div class="questions">
  {#if $queryResult.isLoading}
    <span class="message">Loading...</span>
  {:else if $queryResult.error}
    <span class="message">Error: {$queryResult.error.message}</span>
  {:else}
    {#each $queryResult.data.sort(sortQuestions) as question}
      <Question {...question} />
    {/each}
  {/if}
</div>
<div class="ask">
  <Ask bind:scrollId={scrollId} />
</div>

<style>
  div {
    margin: auto;
    border: thin solid #ddd;
    background-color: #eee;
    max-width: 75ex;
  }

  div.options {
    border-radius: 0.5em 0.5em 0 0 ;
    border-bottom: none;
  }
  div.options * {
    font-size: small;
    color: #666;
  }

  div.questions {
    height: 70vh;
    overflow-y: auto;
  }

  div.ask {
    border-radius: 0 0 0.5em 0.5em;
    border-top: none;
  }

  span.message {
    display: block;
    width: 100%;
    margin-top: 20vh;
    text-align: center;
    font-size: larger;
  }

  span.sort {
    margin-left: 1.3em;
  }

  button {
    margin: 0;
    background-color: #eee;
    border: none;
    padding-left: 2ex;
    padding-right: 2ex;
    cursor: pointer;
  }

  button.sortUp, button.sortDown {
    background-color: #ddd;
  }

  button::after {
    display: inline-block;
    width: 1ex;
    padding-left: 1ex;
    content: "\a0";
  }

  button.sortUp::after {
    content: "▴";
  }

  button.sortDown::after {
    content: "▾";
  }
</style>
