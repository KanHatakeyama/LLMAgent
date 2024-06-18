import io
import contextlib


def parse_record(record):

    problem = record["question_ja"]
    text_ans = record["generated_solution_ja"]

    try:
        # 答えは boxed {123}の形式
        ans_number_pos1 = text_ans.rfind("Boxed {")
        ans_number_pos1_ = text_ans.rfind("boxed {")
        ans_number_pos1 = max(ans_number_pos1, ans_number_pos1_)
        ans_number_pos2 = text_ans.rfind("}")
        ans_number = text_ans[ans_number_pos1+7:ans_number_pos2]
    except:
        problem = ""
        ans_number = ""
    return problem, ans_number


def eval_answer(code_block, answer, verbose=False):
    try:
        output = exec_command(code_block)
    except:
        return False

    if verbose:
        print("answer: ", answer)
        print("predicted: ", output)

    # 文字列での判定
    if output == answer:
        return True

    # 小数での判定
    try:
        if float(output) == float(answer):
            return True
    except:
        pass

    # 答えが整数の場合､整数での判定
    try:
        if float(answer) == int(answer):
            if int(output) == int(answer):
                return True
    except:
        pass
    return False


def exec_command(code_block):
    # Create a string buffer to capture the output
    str_buffer = io.StringIO()
    # Redirect stdout to the string buffer
    with contextlib.redirect_stdout(str_buffer):
        try:
            exec(code_block)
        except Exception as e:
            print(f"Error executing Code Block {i}: {e}")
    # Get the output from the string buffer
    output = (str_buffer.getvalue())
    str_buffer.close()

    return output.strip()
