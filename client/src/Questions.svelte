<script>
  import { useQuery } from '@sveltestack/svelte-query'
  import Question from './Question.svelte'

  async function fetchQuestions() {
    const response = await fetch('http://localhost:8000/questions')
    if (!response.ok) {
      throw new Error('Failure to fetch questions')
    }
    return await response.json()
  }

  const queryResult = useQuery('questions', fetchQuestions)
</script>

{#if $queryResult.isLoading}
  <span>Loading...</span>
{:else if $queryResult.error}
  <span>Error: {$queryResult.error.message}</span>
{:else}
  {#each $queryResult.data as question}
    <Question {...question} />
  {/each}
{/if}
