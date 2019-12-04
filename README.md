# drawTree
This program would read a config file and create a tree base on the file. Using a tab to generate a subtree below previous node. You can also use spaces to create a subtree with -t option. Specifying a config file with -c option, and saving output to a file with -o option.

## Run example.conf
<pre><code>
$ python drawTree.py 
home
  └ken
     ├Desktop
     │  └project
     │     └drawTree
     │        ├drawTree.py
     │        └example.conf
     ├Downloads
     ├Documents
     ├Public
     ├Videos
     ├Pictures
     └Musics
</code><pre>
