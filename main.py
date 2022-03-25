try:
    import random
    import os
    from sys import argv as args
    import json
    import getpass
    try:
        import playsound
        print(getpass.getuser())
        if os.name == "posix" and getpass.getuser() == "root" or os.name=="nt":
            music = True
        else:
            music = False
    except ImportError:
        music = False

    file, words, indx, tries, letters, pov, povlist, cword, stats = "", [], 0, 10, set(), "", [], "", {"acertos": 0,
                                                                                                       "erros": 0}
    ldmode = False
    info = {}


    def settings(setting):

        if os.name != "posix":
                script_dir = os.path.dirname(__file__)
        else:
            script_dir = "/".join(os.path.realpath(__file__).split("/")[:-1])

        config = open(f"{script_dir}/config.file", "r").readlines()
        for line in config:
            if line.startswith(setting):
                return line.split("=")[1].strip()


#    def ost(id):
#        global music
#        
#        if music:
#
#            if settings("music") == "0":
#                music = False
#                return
#
#            if os.name != "posix":
#                script_dir = os.path.dirname(__file__)
#            else:
#                script_dir = "/".join(os.path.realpath(__file__).split("/")[:-1])
#            try:
#                playsound.playsound(f"{script_dir}/ost/{id}.mp3")
#            except Exception as e:
#                print(e)
#                music = False
#            input()


    def clear():
        if os.name == 'nt':
            os.system('cls')
        elif os.name == 'posix':
            os.system('clear')


    def reset(mode="normal", wd=None, customwds=False):
        global cword
        global pov
        global povlist
        global tries
        global letters
        global words

        back = words[:]
        nt = 0
        try:
            if mode == "custom":
                cword = wd
                nt = 1
        except IndexError:
            pass

        if nt != 1:
            if mode == "normal" and not customwds:
                cword = random.choice(words)
            elif customwds:
                script_dir = os.path.dirname(__file__)
                if os.name == 'posix':
                    script_dir = os.path.realpath(__file__).split("/")[:-1]
                
                cwpath = '/'.join(script_dir) if os.name == 'posix' else script_dir + "/custom/words"
                if not os.path.exists(cwpath):
                    os.mkdir(cwpath)

                n = 0
                lista = os.listdir(cwpath)
                for i in lista:
                    n += 1
                    print(f"[{n}] {i}")

                if not lista:
                    print("\nNenhum arquivo!\n")
                    return 0

                try:
                    lsta = int(input("\nQual lista escolher: "))
                except (ValueError, TypeError):
                    return 0

                if lsta > len(lista):
                    print("\nLista inválida!")
                    return 0
                else:
                    n = -1
                    fle = open(f"{cwpath}/{lista[lsta - 1]}", "r").readlines()
                    words = fle
                    for word in words:
                        n += 1
                        words[n] = word.replace("\n", "")

                    try:
                        cword = random.choice(words)
                    except IndexError:
                        print("\nLista vazia!")
                        words = back
                        return 0

        cword = cword.lower()
        pov = "_" * len(cword)
        povlist = [x for x in pov]
        tries = 10
        letters = set()


    def wannacontinue():
        while True:
            if len(args) > 1:
                if args[1] == "custom":
                    exit(0)

            usinput = input("\nQuer continuar? ")
            if usinput.lower() in "sy":
                reset()
                break
            elif usinput.lower() in "n":
                exit(0)
            else:
                print("Opção inválida!")


    def difficulty(argx, wod=""):
        global file
        global words
        global indx

        indx = -1
        if argx == "hard":
            file = "palavras"
        elif argx == "easy":
            file = "palavras_fáceis"

        if argx != "custom":
            words = open(f"{file}.txt", "r").readlines()
            for word in words:
                indx += 1
                word = word.replace("\n", "")
                words[indx] = word
            reset()
        else:
            reset(mode="custom", wd=wod)

        indx = -1


    def playerstat(tp):
        global stats

        if tp == 0:
            stats["acertos"] += 1
        elif tp == 1:
            stats["erros"] += 1
        else:
            print("Erro! Erro! Erro!")


    def save():
        global stats
        global tries
        global letters
        global pov
        global povlist
        global cword
        global words

        lletters = list(letters)
        data = {
            "stats": stats,
            "tries": tries,
            "letters": lletters,
            "pov": pov,
            "povlist": povlist,
            "cword": cword,
            "words": words
        }

        opt = input("\nDeseja salvar? ")
        if opt.lower() in "sy":

            # Funcionou assim, não sei por que. NÃO MEXE!
            saves_dir = os.path.dirname(__file__) + "/saves"
            if os.name == 'posix':
                saves_dir = os.path.realpath(__file__).split("/")[:-1]
                saves_dir = "/".join(saves_dir) + "/saves"
                '/'.join(saves_dir)

            if not os.path.exists(saves_dir):
                os.mkdir(saves_dir)

            saves = os.listdir(saves_dir)
            if len(saves) == 0:
                save_name = input("Qual o nome do seu save? ")
            else:
                n = 0
                for i in saves:
                    n += 1
                    print(f"[{n}] {i.replace('.json', '')}")

                neworold = ""
                save_name = ""
                while neworold not in ["e", "n"]:
                    neworold = input("Salvar em um existente ou criar um novo? [n/e] ")
                    neworold = neworold.lower()
                    if neworold == "n":
                        save_name = input("Qual o nome do seu save? ")
                    elif neworold == "e":
                        opt = input("Salvar no save:  ")
                        save_name = saves[int(opt) - 1].replace('.json', '')
                    else:
                        print("Opção inválida!")

                # Save everything in a json file (create if it doesn't exist)
            open(f"{saves_dir}/{save_name}.json", "w+").write(json.dumps(data, indent=4))
            print(f"{save_name} salvo!")
        elif opt.lower() in "n":
            return 0


    def loadsv():
        global stats
        global tries
        global letters
        global pov
        global povlist
        global cword
        global words

        saves_dir = os.path.dirname(__file__) + "/saves"
        if os.name == 'posix':
            saves_dir = os.path.realpath(__file__).split("/")[:-1]
            saves_dir = "/".join(saves_dir) + "/saves"
            '/'.join(saves_dir)
        saves = os.listdir(saves_dir)
        if len(saves) == 0:
            print("Nenhum save encontrado!")
        else:
            n = 0
            for i in saves:
                n += 1
                print(f"[{n}] {i.replace('.json', '')}")
            opt = input("Qual save deseja carregar? ")
            try:
                return json.loads(open(f"{saves_dir}/{saves[int(opt) - 1]}", "r").read())
            except Exception as e:
                print(f"Erro! Erro! Erro! {e.__context__}")
                return 0


    def delsv():
        saves_dir = os.path.dirname(__file__) + "/saves"
        if os.name == 'posix':
            saves_dir = os.path.realpath(__file__).split("/")[:-1]
            saves_dir = "/".join(saves_dir) + "/saves"

        saves = os.listdir(saves_dir)
        if len(saves) == 0:
            print("Nenhum save encontrado!")
        else:
            n = 0
            for i in saves:
                n += 1
                print(f"[{n}] {i.replace('.json', '')}")
            opt = input("Qual save deseja apagar? ")
            confirm = input("Tem certeza? ")
            if confirm.lower() in "sy":
                try:
                    os.remove(f"{saves_dir}/{saves[int(opt) - 1]}")
                    print(f"{saves[int(opt) - 1]} apagado!")
                except Exception as e:
                    print(f"Erro! Erro! Erro! {e.__context__}")


    def cwl():
        modo = input("Deseja criar ou deletar uma lista de palavras? [c/d] ")
        cwlist = os.path.dirname(__file__) + "/custom/words"
        if os.name == 'posix':
            cwlist = os.path.realpath(__file__).split("/")[:-1]
            cwlist = "/".join(cwlist) + "/custom/words"

        if not os.path.exists(cwlist):
            os.mkdir(cwlist)
        if modo.lower() in "cd":
            if modo.lower() == "c":
                lista = input("Qual o nome da lista? ")

                filex = open(f"{cwlist}/{lista}.txt", "w+")

                palavras = []
                stop = False
                while not stop:
                    palavras.append(input("Digite uma palavra (// para terminar): "))
                    if palavras[-1] == "//":
                        del palavras[-1]
                        stop = True

                filex.write('\n'.join(palavras))
                filex.close()
            elif modo.lower() == "d":
                listas = os.listdir(cwlist)
                for i in listas:
                    print(f"[{listas.index(i) + 1}] {i.replace('.txt', '')}")
                try:
                    lista = int(input("Qual lista apagar: "))

                    if os.path.exists(f"{cwlist}/{listas[lista - 1]}"):
                        os.remove(f"{cwlist}/{listas[lista - 1]}")
                except (ValueError, TypeError):
                    print("Opção inválida!")


    if len(args) > 1:
        if args[1] == "custom":
            difficulty("custom", wod=args[2])
        else:
            difficulty(args[1])
    else:
        difficulty("easy")


    def main():
        global indx
        global tries
        global letters
        global pov
        global povlist
        global ldmode
        global cword
        global words
        global stats
        
        information = {}
        while True:
            if not ldmode:
                clear()
                povlist = [x for x in pov]
                print(pov.replace("", " "))
                uinput = input(f"""
Letras: {' '.join(letters)}
Acertos: {stats["acertos"]}, Erros: {stats["erros"]}
Tentativas: {tries}
Tamanho: {len(cword)} caractere(s)
Palavra ou letra: """)
                if len(uinput) >= 2:
                    if cword == uinput:
                        print("Acerto!")
#                        ost(2)
                        playerstat(0)
                        wannacontinue()
                    else:
                        tries -= 1
#                        ost(1)
                elif len(uinput) == 1 and uinput[0] != "/":
                    if uinput not in letters:
                        letters.add(uinput)
                        if uinput in cword:
                            for i in range(len(cword)):
                                if cword[i] == uinput:
                                    povlist[i] = uinput
#                            ost(2)
                            pov = ''.join(povlist)
                            if '_' not in pov:
                                print("Fim de jogo.")
                                playerstat(0)
#                                ost(3)
                                wannacontinue()
                        else:
                            tries -= 1
#                            ost(1)
                elif len(uinput) <= 0:
                    print("Escreva alguma coisa.")
                    input()
                elif uinput[0] == "/":
                    print("""
[0] - Fácil
[1] - Difícil
[2] - Reiniciar
[3] - Customizado
[4] - Salvar
[5] - Carregar save
[6] - Deletar save
[7] - Usar lista de palavras customizada
[8] - Criar ou deletar lista de palavras customizada
[e] - Sair
[c] - Cancelar""")
                    opt = input(f"Opção: ")
                    if opt == "0":
                        difficulty("easy")
                    elif opt == "1":
                        difficulty("hard")
                    elif opt == "2":
                        reset()
                    elif opt == "3":
                        reset(mode="custom", wd=input(f"\nPalavra: "))
                    elif opt == "4":
                        save()
                    elif opt == "5":
                        information = loadsv()
                        if information != 0:
                            ldmode = True
                    elif opt == "6":
                        delsv()
                    elif opt == "7":
                        reset(customwds=True)
                    elif opt == "8":
                        cwl()
                    elif opt == "e":
                        exit(0)
                    elif opt == "c":
                        print("Opa, voltando ao jogo.")
                if tries == 0:
                    print(f"Perdeu. A palavra era {cword}!")
                    playerstat(1)

                    wannacontinue()
            elif ldmode:
                # load information keys on each erquivalent var
                if "tries" in information:
                    tries = information["tries"]
                if "letters" in information:
                    letters = set(information["letters"])
                if "pov" in information:
                    pov = information["pov"]
                if "povlist" in information:
                    povlist = information["povlist"]
                if "cword" in information:
                    cword = information["cword"]
                if "stats" in information:
                    stats = information["stats"]
                if "words" in information:
                    words = information["words"]
                indx = -1
                ldmode = False


    if __name__ == "__main__":
        main()

except (KeyboardInterrupt, EOFError):
    print("\n\nFim de jogo.")
