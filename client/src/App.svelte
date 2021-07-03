<script>
  import { QueryClient, QueryClientProvider } from '@sveltestack/svelte-query'
  import Questions from './Questions.svelte'

  const queryClient = new QueryClient()
</script>

<QueryClientProvider client={queryClient}>
  <h1>Questions</h1>
  <Questions />
</QueryClientProvider>
