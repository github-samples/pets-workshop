---
applyTo: "**/*.svelte"
---

# Svelte Component Guidelines for Tailspin Shelter

Essential patterns for writing Svelte 5.23+ components with TypeScript in the dark-themed Tailspin Shelter application.

## Core Principles

1. **TypeScript First** - Always use TypeScript for type safety
2. **Dark Theme** - Use slate color palette (`bg-slate-800`, `text-slate-100`, `border-slate-700`)
3. **Responsive** - Mobile-first with Tailwind responsive prefixes
4. **Accessibility** - Semantic HTML and ARIA attributes
5. **Test Identifiers** - Always include `data-testid` attributes for E2E testing

> 📋 **Reference**: See [`test-identifiers.md`](./test-identifiers.md) for complete list of required test IDs

## Basic Component Structure

```svelte
<script lang="ts">
    import { onMount } from 'svelte';
    
    interface DataItem {
        id: number;
        name: string;
    }
    
    export let data: DataItem[] = [];
    export let title = "Default Title";
    
    let loading = false;
    let error: string | null = null;
    
    $: isEmpty = data.length === 0;
    
    onMount(() => {
        // Initialize component
    });
</script>

<!-- Always include data-testid for containers -->
<div data-testid="component-container">
    <h2 class="text-2xl font-medium mb-6 text-slate-100" data-testid="component-title">
        {title}
    </h2>
    
    {#if loading}
        <!-- Loading state with test ID -->
        <div data-testid="component-loading">
            <!-- Loading content -->
        </div>
    {:else if error}
        <!-- Error state with test ID -->
        <div data-testid="component-error">
            <p data-testid="error-message">{error}</p>
        </div>
    {:else}
        <!-- Main content with test ID -->
        <div data-testid="component-content">
            <!-- Content here -->
        </div>
    {/if}
</div>
```

## API Data Fetching

```svelte
<script lang="ts">
    import { onMount } from 'svelte';
    
    interface ApiData {
        id: number;
        name: string;
    }
    
    export let apiData: ApiData[] = [];
    let loading = true;
    let error: string | null = null;
    
    const fetchData = async () => {
        try {
            const response = await fetch('/api/endpoint');
            if (response.ok) {
                apiData = await response.json();
            } else {
                error = `Failed to fetch: ${response.status}`;
            }
        } catch (err) {
            error = `Error: ${err instanceof Error ? err.message : String(err)}`;
        } finally {
            loading = false;
        }
    };
    
    onMount(fetchData);
</script>

<div data-testid="api-component-container">
    {#if loading}
        <div class="animate-pulse bg-slate-800/60 rounded-xl p-6" data-testid="api-component-loading">
            <div class="h-6 bg-slate-700 rounded w-3/4 mb-3"></div>
            <div class="h-4 bg-slate-700 rounded w-1/2"></div>
        </div>
    {:else if error}
        <div class="bg-red-500/20 border border-red-500/50 text-red-400 rounded-xl p-6" data-testid="api-component-error">
            <p data-testid="error-message">{error}</p>
        </div>
    {:else if apiData.length === 0}
        <div class="text-center py-12 bg-slate-800/50 rounded-xl border border-slate-700" data-testid="api-component-empty">
            <p class="text-slate-300" data-testid="empty-message">No data available.</p>
        </div>
    {:else}
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="api-component-grid">
            {#each apiData as item (item.id)}
                <div data-testid={`item-${item.id}`} data-item-id={item.id}>
                    <h3 data-testid={`item-name-${item.id}`}>{item.name}</h3>
                    <!-- More item content -->
                </div>
            {/each}
        </div>
    {/if}
</div>
```

## Dark Theme Card Pattern

```svelte
<!-- Basic card -->
<div class="bg-slate-800/60 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
    <h3 class="text-xl font-semibold text-slate-100 mb-2">{title}</h3>
    <p class="text-slate-400 mb-4">{description}</p>
    <button class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
        Action
    </button>
</div>

<!-- Interactive card with hover effects -->
<a 
    href="/link" 
    class="group block bg-slate-800/60 backdrop-blur-sm rounded-xl border border-slate-700/50 hover:border-blue-500/50 hover:shadow-xl transition-all duration-300 hover:translate-y-[-6px]"
>
    <div class="p-6 relative">
        <div class="absolute inset-0 bg-gradient-to-r from-blue-600/10 to-purple-600/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
        <div class="relative z-10">
            <h3 class="text-xl font-semibold text-slate-100 group-hover:text-blue-400 transition-colors">{title}</h3>
            <div class="mt-4 text-blue-400 font-medium flex items-center">
                <span>View details</span>
                <svg class="h-4 w-4 ml-1 transform group-hover:translate-x-2 transition-transform" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
            </div>
        </div>
    </div>
</a>
```

## Form Handling

```svelte
<script lang="ts">
    let formData = { name: '', email: '' };
    let errors: Record<string, string> = {};
    let submitting = false;
    
    const handleSubmit = async (event: Event) => {
        event.preventDefault();
        errors = {};
        
        if (!formData.name.trim()) errors.name = 'Name required';
        if (!formData.email.trim()) errors.email = 'Email required';
        if (Object.keys(errors).length > 0) return;
        
        submitting = true;
        try {
            await fetch('/api/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            formData = { name: '', email: '' };
        } finally {
            submitting = false;
        }
    };
</script>

<form on:submit={handleSubmit} class="space-y-4">
    <div>
        <label class="block text-slate-300 mb-2">Name</label>
        <input
            bind:value={formData.name}
            class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-slate-100 focus:border-blue-500 transition-colors"
            class:border-red-500={errors.name}
        >
        {#if errors.name}<p class="text-red-400 text-sm mt-1">{errors.name}</p>{/if}
    </div>
    
    <button
        type="submit"
        disabled={submitting}
        class="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 text-white px-6 py-3 rounded-lg transition-colors"
    >
        {submitting ? 'Submitting...' : 'Submit'}
    </button>
</form>
```

## Component Events

```svelte
<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    
    export let items: Item[] = [];
    
    const dispatch = createEventDispatcher<{
        select: { id: number; item: Item };
    }>();
    
    const handleSelect = (item: Item) => {
        dispatch('select', { id: item.id, item });
    };
</script>

<!-- Usage: <MyComponent {items} on:select={handleSelection} /> -->
```

## Accessibility & Testing

```svelte
<!-- Semantic HTML with test attributes -->
<div role="region" aria-labelledby="section-title" data-testid="item-list">
    <h2 id="section-title" class="text-2xl text-slate-100 mb-6">Items</h2>
    
    <ul class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each items as item (item.id)}
            <li>
                <button
                    aria-label="View {item.name}"
                    data-testid="item-{item.id}"
                    class="w-full text-left bg-slate-800/60 rounded-xl p-6 hover:bg-slate-800/80 transition-colors"
                    on:click={() => handleSelect(item)}
                >
                    <h3 class="text-xl font-semibold text-slate-100">{item.name}</h3>
                </button>
            </li>
        {/each}
    </ul>
</div>
```

## Key Patterns Summary

- **TypeScript interfaces** for all data structures
- **Dark theme colors**: `bg-slate-800`, `text-slate-100`, `border-slate-700`
- **Hover effects**: `transition-all duration-300`, `group-hover:` classes
- **Loading skeletons**: `animate-pulse` with `bg-slate-700` placeholders
- **Error handling**: Red backgrounds with `bg-red-500/20` and `text-red-400`
- **Responsive grids**: `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3`
- **Accessibility**: Use semantic HTML, ARIA labels, and `data-testid` attributes
