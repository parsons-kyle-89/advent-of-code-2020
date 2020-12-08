from . import main


def test_main() -> None:
    main.main()


def test_normal_termination() -> None:
    raw_program = """
        nop +0
        acc +1
        jmp +4
        acc +3
        jmp -3
        acc -99
        acc +1
        nop -4
        acc +6
    """.strip()
    program = [
        main.parse_instruction(raw_instruction.strip())
        for raw_instruction in raw_program.splitlines()
    ]
    interpreter = main.TracingInterpreter(program)
    termination_reason = interpreter.run()
    assert termination_reason == main.TerminationReason.NormalTermination


def test_patch_program() -> None:
    raw_program = """
        nop +0
        acc +1
        jmp +4
        acc +3
        jmp -3
        acc -99
        acc +1
        jmp -4
        acc +6
    """.strip()

    raw_patch = """
        nop +0
        acc +1
        jmp +4
        acc +3
        jmp -3
        acc -99
        acc +1
        nop -4
        acc +6
    """.strip()

    program = [
        main.parse_instruction(raw_instruction.strip())
        for raw_instruction in raw_program.splitlines()
    ]
    expected_patch = [
        main.parse_instruction(raw_instruction.strip())
        for raw_instruction in raw_patch.splitlines()
    ]

    actual_patch = main.patch_program(program)
    assert actual_patch == expected_patch
