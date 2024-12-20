public class Solver<L extends ILits>
extends java.lang.Object
implements ISolver, UnitPropagationListener, Learner
The backbone of the library providing the modular implementation of a MiniSAT (Chaff) like solver.

ield Summary
 org.sat4j.minisat.core.Solver.ISimplifier	EXPENSIVE_SIMPLIFICATION
           
static org.sat4j.minisat.core.Solver.ISimplifier	NO_SIMPLIFICATION
           
 org.sat4j.minisat.core.Solver.ISimplifier	SIMPLE_SIMPLIFICATION
           
 
Constructor Summary
Solver(AssertingClauseGenerator acg, LearningStrategy<L> learner, DataStructureFactory<L> dsf, IOrder<L> order, RestartStrategy restarter)
          creates a Solver without LearningListener.
Solver(AssertingClauseGenerator acg, LearningStrategy<L> learner, DataStructureFactory<L> dsf, SearchParams params, IOrder<L> order, RestartStrategy restarter)
           
 
Method Summary
 void	addAllClauses(IVec<IVecInt> clauses)
          Create clauses from a set of set of literals.
 IConstr	addAtLeast(IVecInt literals, int degree)
          Create a cardinality constraint of the type "at least n of those literals must be satisfied"
 IConstr	addAtMost(IVecInt literals, int degree)
          Create a cardinality constraint of the type "at most n of those literals must be satisfied"
 IConstr	addClause(IVecInt literals)
          Create a clause from a set of literals The literals are represented by non null integers such that opposite literals a represented by opposite values.
 IConstr	addPseudoBoolean(IVecInt literals, IVec<java.math.BigInteger> coeffs, boolean moreThan, java.math.BigInteger degree)
          Create a Pseudo-Boolean constraint of the type "at least n of those literals must be satisfied"
 int	analyze(Constr confl, Handle<Constr> outLearntRef)
           
 boolean	assume(int p)
           
 void	claBumpActivity(Constr confl)
          Propagate activity to a constraint
 void	clearLearntClauses()
           
 int	decisionLevel()
           
static int	decode2dimacs(int p)
          decode the internal representation of a literal into Dimacs format.
 boolean	enqueue(int p)
          Satisfait un litt?
 boolean	enqueue(int p, Constr from)
          Put the literal on the queue of assignments to be done.
 int[]	findModel()
          Look for a model satisfying all the clauses available in the problem.
 int[]	findModel(IVecInt assumps)
          Look for a model satisfying all the clauses available in the problem.
 DataStructureFactory<L>	getDSFactory()
           
 IConstr	getIthConstr(int i)
          returns the ith constraint in the solver.
 IOrder<L>	getOrder()
           
 IVecInt	getOutLearnt()
           
 java.util.Map<java.lang.String,java.lang.Number>	getStat()
          To obtain a map of the available statistics from the solver.
 SolverStats	getStats()
           
 int	getTimeout()
          Useful to check the internal timeout of the solver.
 L	getVocabulary()
           
 boolean	isSatisfiable()
          Check the satisfiability of the set of constraints contained inside the solver.
 boolean	isSatisfiable(IVecInt assumps)
          Check the satisfiability of the set of constraints contained inside the solver.
 void	learn(Constr c)
           
 int[]	model()
          Si un mod?
 boolean	model(int var)
          Provide the truth value of a specific variable in the model.
 int	nConstraints()
          To know the number of constraints currently available in the solver.
 int	newVar()
          Create a new variable in the solver (and thus in the vocabulary).
 int	newVar(int howmany)
          Create howmany variables in the solver (and thus in the vocabulary).
 int	nVars()
          To know the number of variables used in the solver.
 void	printStat(java.io.PrintStream out, java.lang.String prefix)
          Display statistics to the given output stream Please use writers instead of stream.
 void	printStat(java.io.PrintWriter out, java.lang.String prefix)
          Display statistics to the given output writer
 Constr	propagate()
           
 boolean	removeConstr(IConstr co)
          Remove a constraint returned by one of the add method from the solver.
 void	reset()
          Clean up the internal state of the solver.
 void	setDataStructureFactory(DataStructureFactory<L> dsf)
          Change the internatal representation of the contraints.
 void	setExpectedNumberOfClauses(int nb)
          To inform the solver of the expected number of clauses to read.
 void	setOrder(IOrder<L> h)
           
 void	setRestartStrategy(RestartStrategy restarter)
           
 void	setSearchListener(SearchListener sl)
           
 void	setSearchParams(SearchParams sp)
           
 void	setSimplifier(org.sat4j.minisat.core.Solver.ISimplifier simp)
          Setup the reason simplification strategy.
 void	setSimplifier(java.lang.String simp)
          Setup the reason simplification strategy.
 void	setTimeout(int t)
          To set the internal timeout of the solver.
 void	setTimeoutMs(long t)
          To set the internal timeout of the solver.
 boolean	simplifyDB()
           
 java.lang.String	toString()
           
 java.lang.String	toString(java.lang.String prefix)
          Display a textual representation of the solver configuration.
 void	varBumpActivity(int p)
          Update the activity of a variable v.