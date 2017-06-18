#!/usr/bin/env python()
# -*- coding: utf-8 -*-


class Animal(object):
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

    def eat(self):
        print "one cat  %s " % self.name, self.colour, "eating something"

    def shout(self):
        print "one cat %s " % self.name, self.colour, "miao yao ~~"

    def run(self):
        print self.name, self.colour, "playing "

if __name__ == "__main__":
    cat1 = Animal("xiaobai", "white")
    cat1.eat()
    cat1.shout()
    cat1.run()
    print"~"*50
    cat2 = Animal("heihei", "black")
    cat2.eat()
    cat2.shout()
    cat2.run()