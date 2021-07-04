<script>
  import { useMutation, useQueryClient } from '@sveltestack/svelte-query'

  async function postQuestion(question) {
    const response = await fetch('http://localhost:8000/question', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({question: question})
    })
    if (!response.ok) {
      throw new Error('Failure to post question')
    }
    return await response.text()
  }

  export let scrollId = null
  let question = ''
  const queryClient = useQueryClient()
  const mutation = useMutation(postQuestion, {
    onSuccess: async (data) => {
      queryClient.invalidateQueries('questions')
      question = ''
      scrollId = data
    }
  })
  $: disabled = $mutation.isLoading ? "disabled" : ""
</script>

<form action="http://localhost:8000/question" method="POST"
      on:submit|preventDefault={() => $mutation.mutate(question)}>
  {#if $mutation.isError}
    <div class="error">
      Error submitting question: {$mutation.error.message}
    </div>
  {/if}
  <textarea name="question" bind:value={question} disabled={disabled}></textarea>
  <button type="submit" disabled={disabled || !question}>Ask!</button>
</form>

<style>
  form {
    padding: 1em;
    display:flex;
  }

  textarea {
    height: 4em;
    resize: vertical;
    flex-grow: 1;
    border-radius: 0.5em 0 0 0.5em;
  }

  button {
    border-radius: 0 0.5em 0.5em 0;
    border-left: none;
  }

  div.error {
    padding: 1em;
    color: #c00;
    text-align: center;
  }
</style>
