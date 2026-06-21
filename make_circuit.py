"""Generate a full adder circuit diagram as SVG for the slides."""
import schemdraw
from schemdraw import logic
from schemdraw import elements as elm

with schemdraw.Drawing(file="full_adder.svg", show=False) as d:
    d.config(unit=0.5, fontsize=14)

    # --- Gates -----------------------------------------------------------
    xor1 = logic.Xor().at((3, 0)).right()
    and1 = logic.And().at((3, -4)).right()
    xor2 = logic.Xor().at((7, -0.5)).right()
    and2 = logic.And().at((7, -2.5)).right()
    or1 = logic.Or().at((10.5, -3.25)).right()

    # --- Inputs a and b --------------------------------------------------
    # a feeds xor1.in1 and and1.in1
    elm.Line().at(xor1.in1).left().length(2.6).label("a", "left").dot(open=True)
    a_split = (xor1.in1[0] - 2.0, xor1.in1[1])
    elm.Line().at(a_split).to((a_split[0], and1.in1[1])).dot()
    elm.Line().at((a_split[0], and1.in1[1])).to(and1.in1)

    # b feeds xor1.in2 and and1.in2
    elm.Line().at(xor1.in2).left().length(1.4).label("b", "left").dot(open=True)
    b_split = (xor1.in2[0] - 1.0, xor1.in2[1])
    elm.Line().at(b_split).to((b_split[0], and1.in2[1])).dot()
    elm.Line().at((b_split[0], and1.in2[1])).to(and1.in2)

    # --- cin feeds xor2.in2 and and2.in1 --------------------------------
    cin_x = xor2.in2[0] - 1.4
    elm.Line().at(xor2.in2).left().length(1.4).label("cin", "left").dot(open=True)
    elm.Line().at((cin_x, xor2.in2[1])).to((cin_x, and2.in1[1])).dot()
    elm.Line().at((cin_x, and2.in1[1])).to(and2.in1)

    # --- a XOR b  ->  xor2.in1 and and2.in2 -----------------------------
    s1_x = xor1.out[0] + 0.8
    elm.Line().at(xor1.out).right().length(0.8).dot()
    elm.Line().at((s1_x, xor1.out[1])).to((s1_x, xor2.in1[1]))
    elm.Line().at((s1_x, xor2.in1[1])).to(xor2.in1)
    elm.Line().at((s1_x, xor1.out[1])).to((s1_x, and2.in2[1])).dot()
    elm.Line().at((s1_x, and2.in2[1])).to(and2.in2)

    # --- sum output ------------------------------------------------------
    elm.Line().at(xor2.out).right().length(1.4).label("sum", "right").dot(open=True)

    # --- and1 / and2  ->  OR  ->  carry ---------------------------------
    elm.Line().at(and1.out).to((or1.in2[0] - 0.6, and1.out[1])) \
        .to((or1.in2[0] - 0.6, or1.in2[1])).to(or1.in2)
    elm.Line().at(and2.out).to((or1.in1[0] - 0.3, and2.out[1])) \
        .to((or1.in1[0] - 0.3, or1.in1[1])).to(or1.in1)
    elm.Line().at(or1.out).right().length(1.4).label("carry", "right").dot(open=True)
