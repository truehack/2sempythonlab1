#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Tree {
    char key[7];
    double value;
    struct Tree *left;
    struct Tree *right;
    int height;
} Tree;

int max(int a, int b) {
    if (a > b) return a;
    return b;
}

int getHeight(Tree *root) {
    if (root == NULL) return 0;
    return root->height;
}

int getBalance(Tree *root) {
    if (root == NULL) return 0;
    return getHeight(root->left) - getHeight(root->right);
}

Tree *createNode(char *key, double value) {
    Tree *root = (Tree *)malloc(sizeof(Tree));
    if (root == NULL) return NULL;

    strcpy(root->key, key);
    root->value = value;
    root->left = NULL;
    root->right = NULL;
    root->height = 1;

    return root;
}

Tree *rotateRight(Tree *y) {
    Tree *x = y->left;
    Tree *t2 = x->right;

    x->right = y;
    y->left = t2;

    y->height = max(getHeight(y->left), getHeight(y->right)) + 1;
    x->height = max(getHeight(x->left), getHeight(x->right)) + 1;

    return x;
}

Tree *rotateLeft(Tree *x) {
    Tree *y = x->right;
    Tree *t2 = y->left;

    y->left = x;
    x->right = t2;

    x->height = max(getHeight(x->left), getHeight(x->right)) + 1;
    y->height = max(getHeight(y->left), getHeight(y->right)) + 1;

    return y;
}

Tree *insert(Tree *root, char *key, double value) {
    int cmp;

    if (root == NULL) return createNode(key, value);

    cmp = strcmp(key, root->key);

    if (cmp < 0) {
        root->left = insert(root->left, key, value);
    } else if (cmp > 0) {
        root->right = insert(root->right, key, value);
    } else {
        return root;
    }

    root->height = max(getHeight(root->left), getHeight(root->right)) + 1;

    if (getBalance(root) > 1 && strcmp(key, root->left->key) < 0)
        return rotateRight(root);

    if (getBalance(root) < -1 && strcmp(key, root->right->key) > 0)
        return rotateLeft(root);

    if (getBalance(root) > 1 && strcmp(key, root->left->key) > 0) {
        root->left = rotateLeft(root->left);
        return rotateRight(root);
    }

    if (getBalance(root) < -1 && strcmp(key, root->right->key) < 0) {
        root->right = rotateRight(root->right);
        return rotateLeft(root);
    }

    return root;
}

Tree *findMin(Tree *root) {
    if (root == NULL) return NULL;

    while (root->left != NULL) {
        root = root->left;
    }

    return root;
}

Tree *deleteNode(Tree *root, char *key) {
    Tree *temp;
    int cmp;

    if (root == NULL) return NULL;

    cmp = strcmp(key, root->key);

    if (cmp < 0) {
        root->left = deleteNode(root->left, key);
    } else if (cmp > 0) {
        root->right = deleteNode(root->right, key);
    } else {
        if (root->left == NULL || root->right == NULL) {
            temp = root->left ? root->left : root->right;

            if (temp == NULL) {
                temp = root;
                root = NULL;
            } else {
                *root = *temp;
            }

            free(temp);
        } else {
            temp = findMin(root->right);
            strcpy(root->key, temp->key);
            root->value = temp->value;
            root->right = deleteNode(root->right, temp->key);
        }
    }

    if (root == NULL) return NULL;

    root->height = max(getHeight(root->left), getHeight(root->right)) + 1;

    if (getBalance(root) > 1 && getBalance(root->left) >= 0)
        return rotateRight(root);

    if (getBalance(root) > 1 && getBalance(root->left) < 0) {
        root->left = rotateLeft(root->left);
        return rotateRight(root);
    }

    if (getBalance(root) < -1 && getBalance(root->right) <= 0)
        return rotateLeft(root);

    if (getBalance(root) < -1 && getBalance(root->right) > 0) {
        root->right = rotateRight(root->right);
        return rotateLeft(root);
    }

    return root;
}

int search(Tree *root, char *key, double *res) {
    int cmp;

    if (root == NULL) return 0;

    cmp = strcmp(key, root->key);

    if (cmp == 0) {
        *res = root->value;
        return 1;
    } else if (cmp < 0) {
        return search(root->left, key, res);
    } else {
        return search(root->right, key, res);
    }
}

void printTree(Tree *root, FILE *out) {
    if (root == NULL) return;
    printTree(root->left, out);
    fprintf(out, "%s:%.2f ", root->key, root->value);
    printTree(root->right, out);
}

void freeTree(Tree *root) {
    if (root == NULL) return;
    freeTree(root->left);
    freeTree(root->right);
    free(root);
}

int main(void) {
    FILE *input = fopen("input.txt", "r");
    FILE *output = fopen("output.txt", "w");
    Tree *root = NULL;
    int op;
    char key[7];
    double value, res;

    if (input == NULL || output == NULL) {
        printf("File error\n");
        return 1;
    }

    while (fscanf(input, "%d", &op) == 1) {
        if (op == 1) {
            if (fscanf(input, "%6s %lf", key, &value) != 2) break;
            fprintf(output, "1 %s %.2f\n", key, value);
            root = insert(root, key, value);
            fprintf(output, "OK\n");
        } else if (op == 2) {
            if (fscanf(input, "%6s", key) != 1) break;
            fprintf(output, "2 %s\n", key);

            if (search(root, key, &res)) {
                root = deleteNode(root, key);
                fprintf(output, "OK\n");
            } else {
                fprintf(output, "Not found\n");
            }
        } else if (op == 3) {
            fprintf(output, "3\n");
            if (root == NULL) {
                fprintf(output, "Empty\n");
            } else {
                printTree(root, output);
                fprintf(output, "\n");
            }
        } else if (op == 4) {
            if (fscanf(input, "%6s", key) != 1) break;
            fprintf(output, "4 %s\n", key);

            if (search(root, key, &res)) {
                fprintf(output, "%.2f\n", res);
            } else {
                fprintf(output, "Not found\n");
            }
        }
    }

    freeTree(root);
    fclose(input);
    fclose(output);
    return 0;
}