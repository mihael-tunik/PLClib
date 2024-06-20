#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <vector>

#define COMPLETELY_LABELED(x) ((x) == 0x7)

using namespace std;

typedef struct 
{
   int Nxy;
   int Nz;
   
   double x_min;
   double x_max;
   
   double y_min;
   double y_max;
   
   double z_min;
   double z_max;
   
}grid_t;

typedef struct 
{
    double data[2];
}d_pair;

int label_fast(d_pair f_val){ 
    int map[] = {1, 1, 2, 4};
    int r = ((f_val.data[1] >= 0.0) << 1) | (f_val.data[0] >= 0.0);        
    return map[r];
}

double *f_wrapped_vec(int N, double z, void (*ptr)(int, double, double *), double *slice_data_ptr){
    (*ptr)(N, z, slice_data_ptr);
    return slice_data_ptr;   
}

void label_fast_vec(double *slice_data, char *cache, int size){
    int NN = size*size;
    
    for(int l = 0; l < NN; ++l){
        d_pair f_val;       
        f_val.data[0] = slice_data[l], f_val.data[1] = slice_data[NN+l]; 
        cache[l] = label_fast(f_val);
    }
    
}

extern "C" int integer_labeling_3d_vec(grid_t GridDesc, void (*ptr)(int, double, double *), 
                                   double *result, int *size){
    vector <double> x, y, z;
    
    int N = GridDesc.Nxy, Nz = GridDesc.Nz;   
    int NN = N*N, NN_sub = (N-1)*(N-1);

    unsigned long long cnt = 0, iter_cnt = 0, grid_size = Nz - 1;
    
    char *cache_prev = new char[NN], *cache_next = new char[NN], *tmp; 
    double *slice_data_ptr = new double[2*NN];
    
    grid_size *= NN_sub;
    
    x.resize(N), y.resize(N), z.resize(Nz);
    
    printf("GridDecs data: \n");
    printf("Nxy: %i, Nz: %i\n", N, Nz);
    
    printf("x_min: %lf, x_max: %lf\n", GridDesc.x_min, GridDesc.x_max);
    printf("y_min: %lf, y_max: %lf\n", GridDesc.y_min, GridDesc.y_max);
    printf("z_min: %lf, z_max: %lf\n", GridDesc.z_min, GridDesc.z_max);
    
    for(int i = 0; i < N; ++i){
        x[i] = GridDesc.x_min + (GridDesc.x_max - GridDesc.x_min)*i/(N-1);
        y[i] = GridDesc.y_min + (GridDesc.y_max - GridDesc.y_min)*i/(N-1);
    }
        
    for(int i = 0; i < Nz; ++i){
        z[i] = GridDesc.z_min + (GridDesc.z_max - GridDesc.z_min)*i/(Nz-1);
    }
        
    label_fast_vec(f_wrapped_vec(N, z[0], ptr, slice_data_ptr), cache_prev, N);
       
    for(int k = 0; k < Nz-1; ++k){  
        label_fast_vec(f_wrapped_vec(N, z[k+1], ptr, slice_data_ptr), cache_next, N);
               
        for(int l = 0; l < NN; )
            if((l / N) != N-1 && (l % N) != N-1){
            
                char label_flags = (cache_prev[l] | cache_prev[l + N] | cache_next[l] | cache_next[l + N]);
                ++l;
                label_flags |= (cache_prev[l] | cache_prev[l + N] | cache_next[l] | cache_next[l + N]);
            
                iter_cnt++;
 
                if(iter_cnt % 100000 == 0)
                    cout << iter_cnt << " cubes checked from " << grid_size << endl;                
            
                if(COMPLETELY_LABELED(label_flags)){
                    result[3*cnt    ] = x[(l - 1) / N];
                    result[3*cnt + 1] = y[(l - 1) % N];
                    result[3*cnt + 2] = z[k];
                    
                    ++cnt;
                }
            }else
                 ++l;
                 
        tmp        = cache_prev;
        cache_prev = cache_next;
        cache_next = tmp;
    }
    
    *size = cnt * 3;
    
    cout << cnt << "  completely labeled cubes found, " << grid_size << " checked!" << endl;
    
    delete[] cache_prev;
    delete[] cache_next;
    delete[] slice_data_ptr;
        
    return 0;    
}
