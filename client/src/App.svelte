<script>
  import { QueryClient, QueryClientProvider } from '@sveltestack/svelte-query'
  import Questions from './Questions.svelte'

  const queryClient = new QueryClient()
</script>

<QueryClientProvider client={queryClient}>
  <Questions />
</QueryClientProvider>
