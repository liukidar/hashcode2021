# def simulation(conf):
    # D = max_durata_da_input_file
    # points = 0
    # strade = {strada:0 for strada in strade}      # 0 è il numero di macchine che hanno dovuto aspettare 
    # for range(D):    # ad ogni timestep
        # for car in cars:
            # move cars one step
            # if car.has_reached_target:
                # points += compute_points(t)

            # if car.is_waiting:
                # strade[car.current_street] += 1

        # update semafori

        

    # return points, strade


# OTTIMIZAZIONE

# conf = {strada:1 for strada in strade}      # 1 secondo ad ogni strada
# for ever:
    # result, strade = simulation(conf)
    # aggiusta conf: aggiungi un secondo alle strade che fanno aspettare macchine, togli un secondo alle strade dove non aspetta nessuno
