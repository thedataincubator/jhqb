<script>
  import { useMutation, useQueryClient } from '@sveltestack/svelte-query'

  async function postQuestion(question) {
    const response = await fetch(`${jhdata.prefix}question`, {
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
  const questionLimit = 2048
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

<form on:submit|preventDefault={() => $mutation.mutate(question)}>
  {#if $mutation.isError}
    <div class="error">
      Error submitting question: {$mutation.error.message}
    </div>
  {/if}
  <div class="entry">
    <textarea name="question" bind:value={question} disabled={disabled} placeholder="Markdown accepted"></textarea>
    <button type="submit" disabled={disabled || !question || question.length > questionLimit}>Ask!</button>
  </div>
  {#if question.length > questionLimit}
    <div class="error">Questions are limited to {questionLimit} characters.</div>
  {/if}
</form>

<style>
  form {
    padding: 1em;
  }

  div.entry {
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
