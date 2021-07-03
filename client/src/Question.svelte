<script>
  export let text
  export let creator
  export let created
  export let votes
  export let id
  export let closed
</script>

<div>
  <span>{text}</span>
  <span>{creator}</span>
  <span>{created}</span>
  <span>{votes.length}</span>
</div>
