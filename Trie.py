#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__)


class Node:
    def __init__(self, label=None, data=None):
        self.label = label
        self.data = data
        self.counter = 0
        self.children = dict()

    def addChild(self, key, data=None):
        if not isinstance(key, Node):
            self.children[key] = Node(key, data)
        else:
            self.children[key.label] = key

    def __getitem__(self, key):
        return self.children[key]


class Trie:
    def __init__(self):
        self.head = Node()
        self.wordList = []
        self.wordChecker = dict()
        self.n = 100
        self.min = 0

    def __getitem__(self, key):
        return self.head.children[key]

    def add(self, word):
        current_node = self.head
        word_finished = True

        for i in range(len(word)):
            if word[i] in current_node.children:
                current_node = current_node.children[word[i]]
                if i == len(word) - 1:
                    current_node.counter += 1
                    if current_node.counter > self.min:
                        self.set_most_frequent(word, current_node.counter)
            else:
                word_finished = False
                break

        # For ever new letter, create a new child node
        if not word_finished:
            while i < len(word):
                current_node.addChild(word[i])
                current_node = current_node.children[word[i]]
                if i == len(word) - 1:
                    current_node.counter += 1
                    if current_node.counter > self.min:
                        self.set_most_frequent(word, current_node.counter)
                i += 1

        # Let's store the full word at the end node so we don't need to
        # travel back up the tree to reconstruct the word
        current_node.data = word

    def has_word(self, word):
        if word == '':
            return False
        if word == None:
            raise ValueError('Trie.has_word requires a not-Null string')

        # Start at the top
        current_node = self.head
        exists = True
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                exists = False
                break

        # Still need to check if we just reached a word like 't'
        # that isn't actually a full word in our dictionary
        if exists:
            if current_node.data == None:
                exists = False

        return current_node.counter

    def set_most_frequent(self, word, counter):
        temp = [word, counter]
        list_size = len(self.wordList)

        if len(self.wordList) == self.n:
            if word in self.wordChecker:
                for i in range(0, list_size):
                    if self.wordList[i][0] == word:
                        self.wordList[i][1] += 1
                        break
            else:
                for i in range(0, list_size):
                    if i == list_size - 1 or counter <= self.wordList[i + 1][1]:
                        self.wordList.insert(i, temp)
                        self.wordChecker[word] = 1
                        del self.wordList[0]
                        self.min = self.wordList[0][1]
                        return

        if list_size < self.n:
            if word in self.wordChecker:
                for i in range(0, list_size):
                    if self.wordList[i][0] == word:
                        self.wordList[i][1] += 1
                        break
            else:
                self.wordChecker[word] = 1
                self.wordList.append(temp)

            if len(self.wordList) == self.n:
                self.wordList.sort(key=lambda x: x[1])
                self.min = self.wordList[0][1]

    def get_most_frequent(self):
        self.wordList.sort(key=lambda x: x[1])
        for i in range(0, len(self.wordList)):
            print self.wordList[i][0]
            print self.wordList[i][1]

    def getData(self, word):
        """ This returns the 'data' of the node identified by the given word """
        if not self.has_word(word):
            raise ValueError('{} not found in trie'.format(word))

        # Race to the bottom, get data
        current_node = self.head
        for letter in word:
            current_node = current_node[letter]

        return current_node.data


@app.route("/")
def checker():
    ter = Trie()
    with open('myfile.txt', 'r') as myfile:
        words = myfile.read().replace('\n', '')
    wordCount = 0
    for word in words.split():
        wordCount += 1
        ter.add(word)
    return json.dumps({'wordList': ter.wordList})


if __name__ == "__main__":
    app.run()

# if __name__ == '__main__':
#     """ Example use """
#     with open('myfile.txt', 'r') as myfile:
#         words = myfile.read().replace('\n', '')
#     trie = Trie()
#     wordCount = 0
#     for word in words.split():
#         wordCount += 1
#         trie.add(word)
#
#
#     print wordCount
#
#     trie.get_most_frequent()
#     print trie.has_word('عرض')
