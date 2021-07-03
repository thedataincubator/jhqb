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
  const queryResult = useQuery('questions', fetchQuestions)

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

<div class="questions">
  {#if $queryResult.isLoading}
    <span>Loading...</span>
  {:else if $queryResult.error}
    <span>Error: {$queryResult.error.message}</span>
  {:else}
    {#each $queryResult.data as question}
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

  div.questions {
    border-radius: 0.5em 0.5em 0 0 ;
    height: 70vh;
    overflow-y: scroll;
  }

  div.ask {
    border-radius: 0 0 0.5em 0.5em;
    border-top: none;
  }

  span {
    display: block;
    width: 100%;
    margin-top: 20vh;
    text-align: center;
    font-size: larger;
  }
</style>
