import FemGui
import FreeCAD
import FemToolsCcx
import FemAnalysis
import FemSolverCalculix
import MechanicalMaterial
# import Part

doc = FreeCAD.ActiveDocument

# box = Part.makeBox(10, 10, 10)
box_obj = doc.addObject('Part::Box', 'Box')

FemAnalysis.makeFemAnalysis('Analysis')
FemGui.setActiveAnalysis(FreeCAD.ActiveDocument.Analysis)

# solver
solver_object = FemSolverCalculix.makeFemSolverCalculix('CalculiX')
solver_object.GeometricalNonlinearity = 'linear'
solver_object.SteadyState = True
solver_object.MatrixSolverType = 'default'
solver_object.IterationsControlParameterTimeUse = False
doc.Analysis.Member = doc.Analysis.Member + [solver_object]

# material
material_object = MechanicalMaterial.\
    makeMechanicalMaterial('MechanicalMaterial')
mat = material_object.Material
mat['Name'] = "Steel-Generic"
mat['YoungsModulus'] = "210000 MPa"
mat['PoissonRatio'] = "0.30"
mat['Density'] = "7900 kg/m^3"
material_object.Material = mat
doc.Analysis.Member = doc.Analysis.Member + [material_object]

# fixed_constraint
fixed_constraint = doc.addObject("Fem::ConstraintFixed", "FemConstraintFixed")
fixed_constraint.References = [(doc.Box, "Face1")]
doc.Analysis.Member = doc.Analysis.Member + [fixed_constraint]

# force_constraint
force_constraint = doc.addObject("Fem::ConstraintForce", "FemConstraintForce")
force_constraint.References = [(doc.Box, "Face2")]
force_constraint.Force = 9000000.0
force_constraint.Direction = (doc.Box, ["Edge5"])
force_constraint.Reversed = True
doc.Analysis.Member = doc.Analysis.Member + [force_constraint]

# mesh
femmesh_obj = doc.addObject('Fem::FemMeshShapeNetgenObject', 'Box_Mesh')
femmesh_obj.Shape = doc.Box
femmesh_obj.MaxSize = 1
doc.Analysis.Member = doc.Analysis.Member + [doc.Box_Mesh]

# recompute doc
doc.recompute()

fea = FemToolsCcx.FemToolsCcx()
fea.update_objects()

message = fea.check_prerequisites()  # the string should be empty
if not message:
    fea.reset_all()
    fea.run()
    fea.load_results()
else:
    print("Houston, we have a problem! {}".format(message))
