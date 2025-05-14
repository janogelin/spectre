# Problem Definition

The problem we are trying to solve is that we have a lot of 'strings' that we need to store in such a way that users can search with any prefix. Our service will suggest the next terms matching the given prefix. For example, if our database contains 'cap', 'cat', 'captain', or 'capital', and the user has typed in 'cap', our system should suggest 'cap', 'captain', and 'capital'.

As we have to serve a lot of queries with minimum latency, we need to come up with a scheme that can efficiently store our data such that it can be queried quickly. We can't depend on some database for this; we need to store our index in memory in a highly efficient data structure.

One of the most appropriate data structures that can serve our purpose is the trie. A trie is a tree-like data structure used to store phrases where each node stores a character of the phrase in sequential manner.

We can assume we have a case-insensitive trie. 