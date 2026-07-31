#include <bits/stdc++.h>
using namespace std;
using ll = long long;
using ld = long double;
#define pb push_back
#define mod 1000000007
#define srt(v) sort(v.begin(),v.end())
#define rsrt(v) sort(v.rbegin(),v.rend())
#define OPTIMIZE_IO ios::sync_with_stdio(false); cin.tie(nullptr);
#define setbit(x) __builtin_popcount(x);
#define printp(v) { for(auto &it : v) std::cout << it.first << " " << it.second << std::endl; }
#define printarr(arr) { for(auto &it : arr) std::cout << it << " "; std::cout << std::endl; }
 
void solve(){
    ll n,q;
    cin>>n>>q;
    vector<ll> v(n+1);
    for(ll i=1; i<=n; i++){
        cin>>v[i];
    }
    while(q--){
        ll a,b, ans=0;
        cin>>a>>b;
        unordered_map<ll,ll> mp;
        for(ll i=a; i<=b; i++){
           mp[v[i]]++;
        }
        for(auto it: mp){
        
            ll num=it.second;
            if(num>=2){
                ll m=num-1;
                ll temp=m*(m+1)/2;
                ans+=temp;
            }
        }
        cout<<ans<<endl;

    }

}
int main() {
    OPTIMIZE_IO;
    int t=1;
    //cin>>t;
    while(t--){
        solve();
    }
    return 0;
}