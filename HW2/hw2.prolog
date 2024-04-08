%childOf(X,Y) - X is a child of Y
%Facts for both parents
childOf(andrew,elizabeth).
childOf(andrew,philip).
childOf(anne,elizabeth).
childOf(anne,philip).
childOf(beatrice,andrew).
childOf(beatrice,sarah).
childOf(charles,elizabeth).
childOf(charles,philip).
childOf(diana,kydd).
childOf(diana,spencer).
childOf(edward,elizabeth).
childOf(edward,philip).
childOf(elizabeth,george).
childOf(elizabeth,mum).
childOf(eugenie,andrew).
childOf(eugenie,sarah).
childOf(harry,charles).
childOf(harry,diana).
childOf(james,edward).
childOf(james,sophie).
childOf(louise,edward).
childOf(louise,sophie).
childOf(margaret,george).
childOf(margaret,mum).
childOf(peter,anne).
childOf(peter,mark).
childOf(william,charles).
childOf(william,diana).
childOf(zara,anne).
childOf(zara,mark).

female(anne).
female(beatrice).
female(diana).
female(elizabeth).
female(kydd).
female(louise).
female(margaret).
female(mum).
female(sarah).
female(sophie).
female(zara).

male(andrew).
male(charles).
male(edward).
male(eugenie).
male(george).
male(harry).
male(james).
male(mark).
male(peter).
male(philip).
male(spencer).
male(william).

%base cases for spouse
married(anne,mark).
married(diana,charles).
married(elizabeth,philip).
married(kydd,spencer).
married(mum,george).
married(sarah,andrew).
married(sophie,edward).

%********************************%
%     implement the following    %
%You may add more clauses to help%
%********************************%
% spouse(X,Y) Symmetric version of married
spouse(X,Y) :- married(X,Y).
spouse(X,Y) :- married(Y,X).

%daughterOf(X,Y) - X is the female child of Y
daughterOf(X,Y) :- female(X), childOf(X,Y).

%sonOf(X,Y) - X is the male child of Y
sonOf(X,Y) :- male(X), childOf(X,Y).

% Define sibling relationship
sibling(X,Y) :- parent(Z,X), parent(Z,Y), X \= Y.

% Define parent relationship
parent(X,Y) :- childOf(Y,X).

% brotherOf(X,Y) - X is the male sibling of Y
brotherOf(X,Y) :- male(X), sibling(X,Y).

%sisterOf(X,Y) - X is the female sibling of Y
sisterOf(X,Y) :- female(X), sibling(X,Y).

% grandchildOf(X,Y) - X is a grandchild of Y
grandchildOf(X,Y) :- childOf(X,Z), childOf(Z,Y).

%ancestorOf(X,Y) - X is an ancestor of Y
ancestorOf(X,Y) :- childOf(Y,X).
ancestorOf(X,Y) :- childOf(Y,Z), ancestorOf(X,Z).

%auntOf(X,Y) - X is the aunt of Y
auntOf(X,Y) :- sisterOf(X,Z), parent(Z,Y).

%uncleOf(X,Y) - X is the uncle of Y
uncleOf(X,Y) :- brotherOf(X,Z), parent(Z,Y).

%firstCousinOf(X,Y) - X is the first cousin of Y; i.e. one of X's parents is siblings with one of Y's parents
firstCousinOf(X,Y) :- parent(Z,X), parent(W,Y), sibling(Z,W).

%brotherInLawOf(X,Y) - X is the brother of Y's spouse or X is the male spouse of Y's sibling
brotherInLawOf(X,Y) :- (spouse(Y,Z), brotherOf(X,Z)); (sibling(Y,Z), married(Z,X), male(X)).

% sisterInLawOf(X,Y) - X is the sister of Y's spouse or X is the female spouse of Y's sibling
sisterInLawOf(X,Y) :- (spouse(Y,Z), sisterOf(X,Z)); (sibling(Y,Z), married(X,Z), female(X)).

