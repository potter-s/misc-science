#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef struct {
        double val;
} stack_item;

typedef struct {
	int len;
	stack_item *si;
} stack;

typedef struct {
	int (*fn)(stack *);
	char op;
	int nstack;
} registry;

/*
int stack_cleanup(stack *);
int parse_line(char *);
int rotate_stack_n_up(stack *, int);
int rotate_stack_n_down(stack *, int);
int stack_add(stack *)
int stack_init(stack *);
int stack_switch_top(stack *);
int stack_push(stack *, double);
int stack_top_is_int(stack *, int);
*/

int stack_cleanup(stack *st) {
	st->len = 0;
	free(st->si);
	return 0;
}

	/*
int parse_line(char *line) {
	while (*line && *line != '\n') {
		if (*line == ' ')
			line++;
		if (isalpha(*line)) 
		
	if (*line && *line
}
	*/

// parse line
// clean, extract op and operand

int rotate_stack_n_up(stack *st, int n) {
	double temp;
	int i;
	if (st->len < n)
		return 0;
	temp = st->si[st->len - n].val;
	for (i = st->len - n; i < st->len - 1; i++)
		st->si[i].val = st->si[i + 1].val;
	st->si[i].val = temp;
	return n;
}

int rotate_stack_n_down(stack *st, int n) {
	double temp;
	int i;
	if (st->len < n)
		return 0;
	temp = st->si[st->len - 1].val;
	for (i = st->len - 1; i > st->len - n; i--)
		st->si[i].val = st->si[i - 1].val;
	st->si[i].val = temp;
	return n;
}

int stack_init(stack *st) {
	st->len = 0;
	st->si = NULL;
	return 0;
}

int stack_switch_top(stack *st) {
	rotate_stack_n_down(st, 2);
}

int stack_push(stack *st, double val) {
	st->si = (stack_item *)(realloc(st->si, ++st->len * sizeof(stack_item)));
	st->si[st->len - 1].val = val;
}

int stack_drop(stack *st) {
	st->si = (stack_item *)(realloc(st->si, --st->len * sizeof(stack_item)));
}

double stack_pop(stack *st) {
	double val;
	val = st->si[--st->len].val;
	st->si = (stack_item *)(realloc(st->si, st->len * sizeof(stack_item)));
	return val;
}

double stack_top(stack *st, int n) {
	return st->si[st->len - 1 - n].val;
}

int stack_top_is_int(stack *st, int n) {
	return st->si[st->len - 1 - n].val == (int)st->si[st->len - 1 - n].val;
}

int stack_mult(stack *st)
{
	stack_push(st, stack_pop(st) * stack_pop(st));
}

int stack_add(stack *st)
{
	stack_push(st, stack_pop(st) + stack_pop(st));
}

int stack_sqr(stack *st)
{
	stack_push(st, stack_top(st, 0) * stack_pop(st));
}

int stack_sqrt(stack *st)
{
	stack_push(st, sqrt(stack_pop(st)));
}

int stack_recip(stack *st)
{
	stack_push(st, 1.0 / stack_pop(st));
}

int stack_sub(stack *st)
{
	stack_switch_top(st);
	stack_push(st, stack_pop(st) - stack_pop(st));
}

int stack_div(stack *st)
{
	stack_switch_top(st);
	stack_push(st, stack_pop(st) / stack_pop(st));
}

int register_ops(registry **ppops) {
	*ppops = (registry *) malloc(8 * sizeof(registry));
	registry *pops = *ppops;

	pops->op = '+';
	pops->nstack = 2;
	pops++->fn = &stack_add;
	pops->op = '-';
	pops->nstack = 2;
	pops++->fn = &stack_sub;
	pops->op = '*';
	pops->nstack = 2;
	pops++->fn = &stack_mult;
	pops->op = '/';
	pops->nstack = 2;
	pops++->fn = &stack_div;

	pops->op = 's';
	pops->nstack = 1;
	pops++->fn = &stack_sqr;
	pops->op = 'q';
	pops->nstack = 1;
	pops++->fn = &stack_sqrt;
	pops->op = 'r';
	pops->nstack = 1;
	pops++->fn = &stack_recip;

	pops->op = 'd';
	pops->nstack = 1;
	pops++->fn = &stack_drop;

	return pops - *ppops;
}

int main(int argc, char **argv)
{
	double *val;
	int arg;
	int i;
	size_t len = 0;
	int rt;
	int nops;
	char *op;
	char *line = NULL;
	val = (double *)malloc(sizeof(double));

	op = malloc(3);
	stack st;

	stack_init(&st);

	registry *ops;
	nops = register_ops(&ops);

	printf("\t");
	while (getline(&line, &len, stdin) != EOF) {
		if (sscanf(line, " %lf\n", val)) {
			stack_push(&st, *val);
		}
		// maths operations
		else if (sscanf(line, "%1[+-/*%sqrd]\n", op) && strlen(op) == 1) {
			for (i = 0; i < nops; i++) {
				if (*op == ops[i].op) {
					if (st.len >= ops[i].nstack)
						ops[i].fn(&st);
					else
						printf("Stack length error [%d]\n", st.len);
				}
			}
		}
		// stack operations
		else if (sscanf(line, " %1[pdxR]%lf", op, val) && strlen(op) == 1) {
			switch (*op) {
				case 'R':
					if (*val && *val > 0)
						rotate_stack_n_down(&st, *val);
					else
						rotate_stack_n_up(&st, -*val);
					break;
				case 'x':
					rotate_stack_n_up(&st, 2);
					break;
				case 'd':
					stack_drop(&st);
					break;
				case 'p':
					if (! *val)
						*val = 1;
					//*val--;
					if (st.len <= *val)
						printf("Stack length error [%d]\n", st.len);
					else
						for (int i = *val; i >= 0; i--)
							if (stack_top_is_int(&st, i))
								printf("%d: %d\n", i + 1, (int)stack_top(&st, i));
							else
								printf("%d: %f\n", i + 1, stack_top(&st, i));
					break;
			}
		}
		/*
		else if (sscanf(line, " %1[p]", op) && strlen(op) == 1) {
			if (stack_top_is_int(&st, 0))
				printf("%d: %d\n", 1, (int)stack_top(&st, 0));
			else
				printf("%d: %f\n", 1, stack_top(&st, 0));
		}
		*/
		*val = 0;
		/*
		for (i = 0; i < st.len; i++) {
			if (stack_top_is_int(&st, 0))
				printf("%d: %d\n", i, (int)st.si[i].val);
			else
				printf("%d: %f\n", i, st.si[i].val);
		}
		*/
		if (st.len > 0)
			if (stack_top_is_int(&st, 0))
				printf("%d\t", (int)stack_top(&st, 0));
			else
				printf("%f\t", stack_top(&st, 0));
		else
			printf("\t");
		}

	stack_cleanup(&st);
}
